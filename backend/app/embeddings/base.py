from abc import ABC, abstractmethod
from typing import Any


class BaseEmbeddingModel(ABC):

    @abstractmethod
    def encode(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        raise NotImplementedError

    @property
    @abstractmethod
    def tokenizer(self) -> Any:
        raise NotImplementedError

    @property
    @abstractmethod
    def max_input_length(self) -> int:
        raise NotImplementedError