from unittest.mock import AsyncMock, patch

import pytest

from app.llm.ollama import OllamaLLM


@pytest.mark.anyio
async def test_ollama_llm_generates_text():

    response = {
        "message": {
            "content": "Generated answer."
        }
    }

    with patch(
        "app.llm.ollama.AsyncClient"
    ) as client_class:

        client = client_class.return_value

        client.chat = AsyncMock(
            return_value=response
        )

        llm = OllamaLLM(
            base_url="http://localhost:11434",
            model="qwen3:8b",
        )

        result = await llm.generate(
            instructions="Use only the context.",
            prompt="What is this document about?",
        )

        assert result == "Generated answer."

        client.chat.assert_awaited_once_with(
            model="qwen3:8b",
            messages=[
                {
                    "role": "system",
                    "content": "Use only the context.",
                },
                {
                    "role": "user",
                    "content": "What is this document about?",
                },
            ],
        )