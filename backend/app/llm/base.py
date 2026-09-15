from abc import ABC, abstractmethod


class BaseLLM(ABC):

    @abstractmethod
    async def generate(
        self,
        *,
        instructions: str,
        prompt: str,
    ) -> str:
        raise NotImplementedError