
from typing import List
from chunk import Chunk


class BaseEmbedding:

    def embed_query(self, text: str) -> List[float]:

        pass

    def embed_documents(self, texts: List[str]) -> List[List[float]]:

        pass

    def embed_chunks(self, chunks: List[Chunk], batch_size: int = 256) -> List[Chunk]:

        pass

    @property
    def dimension(self) -> int:

        pass
