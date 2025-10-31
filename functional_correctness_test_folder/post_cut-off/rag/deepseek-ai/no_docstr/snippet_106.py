
from typing import Dict, Any, Union, List
import numpy as np
from langchain.embeddings.base import BaseEmbeddings


class ChromaEmbeddingFunction:
    """Chroma Embedding Function.
    Embeds the text of the chunks using the embedding model and 
    adds the embeddings to the chunks for use in downstream tasks
    like upserting into a vector database.
    Args:
        embedding_model: The embedding model to use.
        **kwargs: Additional keyword arguments.
    """

    def __init__(self, embedding_model: Union[str, BaseEmbeddings] = 'minishlab/potion-retrieval-32M', **kwargs: Dict[str, Any]) -> None:
        """Initialize the ChromaEmbeddingFunction."""
        if isinstance(embedding_model, str):
            from langchain.embeddings import HuggingFaceEmbeddings
            self.embedding_model = HuggingFaceEmbeddings(
                model_name=embedding_model, **kwargs)
        else:
            self.embedding_model = embedding_model

    def name(self) -> str:
        """Return the name of the embedding model for ChromaDB compatibility."""
        if hasattr(self.embedding_model, 'model_name'):
            return self.embedding_model.model_name
        return self.embedding_model.__class__.__name__

    def __call__(self, input: Union[str, List[str]]) -> Union[np.ndarray, List[np.ndarray]]:
        """Call the ChromaEmbeddingFunction."""
        embeddings = self.embedding_model.embed_documents(
            input if isinstance(input, list) else [input])
        if isinstance(input, list):
            return [np.array(embedding) for embedding in embeddings]
        return np.array(embeddings[0])
