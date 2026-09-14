from abc import ABC, abstractmethod


class BaseProcessor(ABC):
    @abstractmethod
    async def extract_text(
        self,
        file_path: str,
    ) -> tuple[str, int, list[str]]:
        raise NotImplementedError