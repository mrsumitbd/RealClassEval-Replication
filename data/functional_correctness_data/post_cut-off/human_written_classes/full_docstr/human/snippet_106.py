from chonkie.embeddings import AutoEmbeddings, BaseEmbeddings
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, Sequence, Union

class ChromaEmbeddingFunction:
    """Chroma Embedding Function.

    Embeds the text of the chunks using the embedding model and 
    adds the embeddings to the chunks for use in downstream tasks
    like upserting into a vector database.

    Args:
        embedding_model: The embedding model to use.
        **kwargs: Additional keyword arguments.

    """

    def __init__(self, embedding_model: Union[str, BaseEmbeddings]='minishlab/potion-retrieval-32M', **kwargs: Dict[str, Any]) -> None:
        """Initialize the ChromaEmbeddingFunction."""
        super().__init__()
        if isinstance(embedding_model, str):
            self.embedding_model = AutoEmbeddings.get_embeddings(embedding_model, **kwargs)
            self._model_name = embedding_model
        elif isinstance(embedding_model, BaseEmbeddings):
            self.embedding_model = embedding_model
            self._model_name = str(embedding_model)
        else:
            raise ValueError('Model must be a string or a BaseEmbeddings instance.')

    def name(self) -> str:
        """Return the name of the embedding model for ChromaDB compatibility."""
        return self._model_name

    def __call__(self, input: Union[str, List[str]]) -> Union['np.ndarray', List['np.ndarray']]:
        """Call the ChromaEmbeddingFunction."""
        if isinstance(input, str):
            return self.embedding_model.embed(input)
        elif isinstance(input, list):
            return self.embedding_model.embed_batch(input)
        else:
            raise ValueError('Input must be a string or a list of strings.')