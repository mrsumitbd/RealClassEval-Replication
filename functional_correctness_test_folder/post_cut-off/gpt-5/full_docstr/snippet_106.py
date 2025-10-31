from typing import Any, Dict, List, Union

import numpy as np

try:
    from langchain_core.embeddings import Embeddings as BaseEmbeddings  # type: ignore
except Exception:
    try:
        from langchain.embeddings.base import Embeddings as BaseEmbeddings  # type: ignore
    except Exception:
        BaseEmbeddings = Any  # Fallback typing if LangChain isn't installed


class ChromaEmbeddingFunction:
    '''Chroma Embedding Function.
    Embeds the text of the chunks using the embedding model and 
    adds the embeddings to the chunks for use in downstream tasks
    like upserting into a vector database.
    Args:
        embedding_model: The embedding model to use.
        **kwargs: Additional keyword arguments.
    '''

    def __init__(self, embedding_model: Union[str, BaseEmbeddings] = 'minishlab/potion-retrieval-32M', **kwargs: Dict[str, Any]) -> None:
        '''Initialize the ChromaEmbeddingFunction.'''
        self._kwargs = dict(kwargs) if kwargs else {}
        self._normalize = bool(self._kwargs.pop("normalize_embeddings", True))
        self._batch_size = int(self._kwargs.pop("batch_size", 32))

        self._is_langchain = False
        self._st_model = None
        self._model_name = None

        if isinstance(embedding_model, str):
            try:
                from sentence_transformers import SentenceTransformer  # type: ignore
            except Exception as e:
                raise ImportError(
                    "sentence-transformers must be installed to use a string embedding model identifier."
                ) from e
            self._st_model = SentenceTransformer(
                embedding_model, **self._kwargs)
            self._model_name = embedding_model
        else:
            # Assume LangChain-like BaseEmbeddings interface
            self._is_langchain = True
            self._lc_model = embedding_model
            # Best-effort name
            self._model_name = getattr(embedding_model, "model", None) or getattr(embedding_model, "model_name", None) \
                or getattr(embedding_model, "__class__", type("X", (), {})).__name__

    def name(self) -> str:
        '''Return the name of the embedding model for ChromaDB compatibility.'''
        return str(self._model_name)

    def __call__(self, input: Union[str, List[str]]) -> Union['np.ndarray', List['np.ndarray']]:
        '''Call the ChromaEmbeddingFunction.'''
        if isinstance(input, str):
            texts = [input]
            single = True
        elif isinstance(input, list) and all(isinstance(t, str) for t in input):
            texts = input
            single = False
        else:
            raise TypeError("Input must be a string or a list of strings.")

        if self._is_langchain:
            # Use LangChain Embeddings interface
            if single and hasattr(self._lc_model, "embed_query"):
                vec = self._lc_model.embed_query(texts[0])
                arr = np.asarray(vec, dtype=np.float32)
                if self._normalize:
                    norm = np.linalg.norm(arr)
                    if norm > 0:
                        arr = arr / norm
                return arr
            else:
                vecs = self._lc_model.embed_documents(texts)
                out = []
                for v in vecs:
                    arr = np.asarray(v, dtype=np.float32)
                    if self._normalize:
                        norm = np.linalg.norm(arr)
                        if norm > 0:
                            arr = arr / norm
                    out.append(arr)
                return out

        # Sentence-Transformers path
        assert self._st_model is not None
        emb = self._st_model.encode(
            texts,
            batch_size=self._batch_size,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=self._normalize,
        )
        if single:
            return np.asarray(emb[0], dtype=np.float32)
        else:
            return [np.asarray(e, dtype=np.float32) for e in emb]
