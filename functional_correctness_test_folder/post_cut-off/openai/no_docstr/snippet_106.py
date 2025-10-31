
from typing import Any, Dict, List, Union
import numpy as np
from langchain.embeddings import BaseEmbeddings
from langchain.embeddings.huggingface import HuggingFaceEmbeddings


class ChromaEmbeddingFunction:
    """
    A wrapper around a LangChain embedding model that can be used with Chroma.
    """

    def __init__(
        self,
        embedding_model: Union[str,
                               BaseEmbeddings] = "minishlab/potion-retrieval-32M",
        **kwargs: Dict[str, Any],
    ) -> None:
        """
        Initialize the embedding function.

        Parameters
        ----------
        embedding_model : Union[str, BaseEmbeddings]
            Either a string specifying the HuggingFace model name or an instance
            of a LangChain BaseEmbeddings subclass.
        **kwargs : Any
            Additional keyword arguments forwarded to the embedding model constructor.
        """
        if isinstance(embedding_model, str):
            # Use HuggingFaceEmbeddings as the default implementation
            self.embeddings: BaseEmbeddings = HuggingFaceEmbeddings(
                model_name=embedding_model, **kwargs
            )
        else:
            self.embeddings = embedding_model

    def name(self) -> str:
        """
        Return the name of the underlying embedding model class.
        """
        return self.embeddings.__class__.__name__

    def __call__(self, input: Union[str, List[str]]) -> Union[np.ndarray, List[np.ndarray]]:
        """
        Compute embeddings for the given input.

        Parameters
        ----------
        input : Union[str, List[str]]
            A single string or a list of strings to embed.

        Returns
        -------
        Union[np.ndarray, List[np.ndarray]]
            The embedding(s) as a NumPy array or a list of arrays.
        """
        if isinstance(input, str):
            # Single query embedding
            return self.embeddings.embed_query(input)
        elif isinstance(input, list):
            # Batch document embeddings
            return self.embeddings.embed_documents(input)
        else:
            raise TypeError(
                f"Unsupported input type {type(input).__name__}. "
                "Expected str or List[str]."
            )
