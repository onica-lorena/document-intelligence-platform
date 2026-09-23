from app.llm.base import BaseLLM
from app.models.chunk import Chunk
from app.repositories.chunk import ChunkRepository
from app.schemas.rag import RAGResponse, RAGSource
from app.services.search import SearchService

class RAGService:

    SYSTEM_INSTRUCTIONS = """
You are a document question-answering assistant.

Answer the user's question using only the provided context.

Rules:
- Answer in the same language as the user's question.
- Do not use outside knowledge.
- Do not invent, assume, or infer facts that are not explicitly supported by the context.
- If the context does not contain enough information to answer,
  clearly say that the answer cannot be determined from the provided documents.
- Preserve the structure, categories, terminology, and relationships explicitly
  established by the source document.
- Do not move, merge, or reclassify information between different sections
  or categories unless the context explicitly supports that relationship.
- Do not add characteristics, relationships, or classifications that are not
  explicitly supported by the context.
- Do not change the meaning or category of a term based on outside knowledge.
- Do not repeat the user's question.
- Do not add meta-comments about the sources, documents, or citations.
- Avoid repeating the same fact when it appears multiple times in the context.
- Keep the answer clear, natural, concise, and proportional to the question.
- When making a factual statement based on the context, include the
  corresponding citation number in the format [1], [2], [3], etc.
- Use only citation numbers that actually exist in the provided context.
""".strip()

    def __init__(
        self,
        search_service: SearchService,
        llm: BaseLLM,
        chunk_repository: ChunkRepository,
    ):
        self.search_service = search_service
        self.llm = llm
        self.chunk_repository = chunk_repository

    async def _expand_context(
        self,
        search_results,
        radius: int = 2,
    ) -> dict[int, list[Chunk]]:

        expanded_context: dict[int, list[Chunk]] = {}

        seen_chunks: set[tuple[str, int]] = set()

        for result_index, result in enumerate(
            search_results,
            start=1,
        ):
            adjacent_chunks = (
                await self.chunk_repository.find_adjacent(
                    document_id=result.document_id,
                    chunk_index=result.chunk_index,
                    radius=radius,
                )
            )

            unique_chunks = []

            for chunk in adjacent_chunks:
                chunk_key = (
                    chunk.document_id,
                    chunk.chunk_index,
                )

                if chunk_key in seen_chunks:
                    continue

                seen_chunks.add(chunk_key)
                unique_chunks.append(chunk)

            expanded_context[result_index] = unique_chunks

        return expanded_context

    async def answer(
        self,
        *,
        query: str,
        limit: int = 5,
        document_id: str | None = None,
    ) -> RAGResponse:

        query = query.strip()

        if not query:
            return RAGResponse(
                answer="Please provide a question.",
                sources=[],
            )

        search_results = await self.search_service.search(
            query=query,
            limit=limit,
            document_id=document_id,
        )

        if not search_results:
            return RAGResponse(
                answer=(
                    "I could not find relevant information "
                    "in the provided documents."
                ),
                sources=[],
            )

        expanded_context = await self._expand_context(
            search_results,
            radius=2,
        )

        context_parts = []
        sources = []

        for index, result in enumerate(
            search_results,
            start=1,
        ):
            chunks = expanded_context[index]

            chunk_parts = []

            for chunk in chunks:
                chunk_parts.append(
                    f"Chunk {chunk.chunk_index} "
                    f"(Page {chunk.page_number}):\n"
                    f"{chunk.text}"
                )

            expanded_text = "\n\n".join(
                chunk_parts
            )

            if not expanded_text:
                expanded_text = (
                    f"Chunk {result.chunk_index} "
                    f"(Page {result.page_number}):\n"
                    f"{result.text}"
                )

            context_parts.append(
                f"[{index}]\n"
                f"Document ID: {result.document_id}\n"
                f"Retrieved chunk: {result.chunk_index}\n"
                f"Expanded context:\n"
                f"{expanded_text}"
            )

            sources.append(
                RAGSource(
                    citation_id=index,
                    document_id=result.document_id,
                    chunk_index=result.chunk_index,
                    text=expanded_text,
                    page_number=result.page_number,
                    score=result.score,
                )
            )

        context = "\n\n".join(context_parts)

        prompt = f"""
Answer the following question using only the provided context.

Question:
{query}

Context:
{context}
""".strip()

        answer = await self.llm.generate(
            instructions=self.SYSTEM_INSTRUCTIONS,
            prompt=prompt,
        )

        return RAGResponse(
            answer=answer,
            sources=sources,
        )