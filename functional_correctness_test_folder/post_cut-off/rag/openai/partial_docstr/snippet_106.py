
from __future__ import annotations

from typing import Any, Dict, List, Union

import numpy as np
from langchain.embeddings.base import BaseEmbeddings
from langchain.embeddings.huggingface import HuggingFaceEmbeddings


class ChromaEmbeddingFunction:
    """Chroma Embedding Function.

    Embeds the text of the chunks using the embedding model and
    adds the embeddings to the chunks for use in downstream tasks
    like upserting into a vector database.
    """

    def __init__(
        self,
        embedding_model: Union[str,
                               BaseEmbeddings] = "minishlab/potion-retrieval-32M",
        **kwargs: Dict[str, Any],
    ) -> None:
        """Initialize the ChromaEmbeddingFunction."""
        if isinstance(embedding_model, str):
            self.embedding_model = HuggingFaceEmbeddings(
                model_name=embedding_model, **kwargs
            )
        else:
            self.embedding_model = embedding_model

    def name(self) -> str:
        """Return the name of the embedding model for ChromaDB compatibility."""
        if isinstance(self.embedding_model, HuggingFaceEmbeddings):
            return self.embedding_model.model_name
        # Fallback: try to get a model_name attribute or use the class name
        return getattr(self.embedding_model, "model_name", self.embedding_model.__class__.__name__)

    def __call__(
        self, input: Union[str, List[str]]
    ) -> Union[np.ndarray, List[np.ndarray]]:
        """Call the ChromaEmbeddingFunction."""
        if isinstance(input, str):
            # embed_query returns a list of floats
            vec = self.embedding_model.embed_query(input)
            return np.array(vec, dtype=np.float32)
        else:
            # embed_documents returns a list of lists of floats
            vecs = self.embedding_model.embed_documents(input)
            return [np.array(v, dtype=np.float32) for v in vecs]
