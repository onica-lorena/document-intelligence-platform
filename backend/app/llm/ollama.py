from ollama import AsyncClient

from app.core.config import settings
from app.llm.base import BaseLLM


class OllamaLLM(BaseLLM):

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
    ):
        self.base_url = (
            base_url
            or settings.OLLAMA_BASE_URL
        )

        self.model = (
            model
            or settings.OLLAMA_MODEL
        )

        self.client = AsyncClient(
            host=self.base_url,
        )

    async def generate(
        self,
        *,
        instructions: str,
        prompt: str,
    ) -> str:

        response = await self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": instructions,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return response["message"]["content"]