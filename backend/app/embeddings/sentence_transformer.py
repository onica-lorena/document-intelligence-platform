from sentence_transformers import SentenceTransformer

from app.embeddings.base import BaseEmbeddingModel


class SentenceTransformerEmbeddingModel(BaseEmbeddingModel):

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ):
        self.model = SentenceTransformer(model_name)

    def encode(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        embeddings = self.model.encode(texts)
        return embeddings.tolist()

    @property
    def tokenizer(self):
        return self.model.tokenizer

    @property
    def max_input_length(self) -> int:
        return self.model.max_seq_length