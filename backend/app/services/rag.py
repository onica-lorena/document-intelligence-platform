from app.llm.base import BaseLLM
from app.schemas.rag import RAGResponse, RAGSource
from app.services.search import SearchService


class RAGService:

    SYSTEM_INSTRUCTIONS = """
You are a document question-answering assistant.

Answer the user's question only using the provided context.

Rules:
- Do not use outside knowledge.
- Do not invent facts.
- If the context does not contain enough information to answer,
  clearly say that the answer cannot be determined from the provided documents.
- When making a factual statement based on the context, include the
  corresponding citation number in the format [1], [2], [3], etc.
- Use only the citation numbers that actually exist in the provided context.
- Keep the answer clear and concise.
""".strip()

    def __init__(
        self,
        search_service: SearchService,
        llm: BaseLLM,
    ):
        self.search_service = search_service
        self.llm = llm

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

        context_parts = []
        sources = []

        for index, result in enumerate(
            search_results,
            start=1,
        ):
            context_parts.append(
                f"[{index}]\n"
                f"Document ID: {result.document_id}\n"
                f"Chunk: {result.chunk_index}\n"
                f"Page: {result.page_number}\n"
                f"Content:\n{result.text}"
            )

            sources.append(
                RAGSource(
                    citation_id=index,
                    document_id=result.document_id,
                    chunk_index=result.chunk_index,
                    text=result.text,
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