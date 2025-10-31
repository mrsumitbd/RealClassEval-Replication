from typing import Any, Dict, List, Union
import numpy as np


class ChromaEmbeddingFunction:
    '''Chroma Embedding Function.
    Embeds the text of the chunks using the embedding model and 
    adds the embeddings to the chunks for use in downstream tasks
    like upserting into a vector database.
    Args:
        embedding_model: The embedding model to use.
        **kwargs: Additional keyword arguments.
    '''

    def __init__(self, embedding_model: Union[str, 'BaseEmbeddings'] = 'minishlab/potion-retrieval-32M', **kwargs: Dict[str, Any]) -> None:
        '''Initialize the ChromaEmbeddingFunction.'''
        if isinstance(embedding_model, str):
            # Assume a from_pretrained or similar method exists
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(embedding_model, **kwargs)
            self._model_name = embedding_model
        else:
            self.model = embedding_model
            self._model_name = getattr(
                embedding_model, 'name', None) or embedding_model.__class__.__name__

    def name(self) -> str:
        '''Return the name of the embedding model for ChromaDB compatibility.'''
        return self._model_name

    def __call__(self, input: Union[str, List[str]]) -> Union['np.ndarray', List['np.ndarray']]:
        '''Call the ChromaEmbeddingFunction.'''
        if isinstance(input, str):
            embedding = self.model.encode(input)
            if not isinstance(embedding, np.ndarray):
                embedding = np.array(embedding)
            return embedding
        else:
            embeddings = self.model.encode(input)
            if not isinstance(embeddings, np.ndarray):
                embeddings = np.array(embeddings)
            return embeddings
