from typing import Union, List, Any, Dict, Optional
import numpy as np

try:
    from langchain_core.embeddings import Embeddings as BaseEmbeddings  # type: ignore
except Exception:
    try:
        from langchain.embeddings.base import Embeddings as BaseEmbeddings  # type: ignore
    except Exception:
        class BaseEmbeddings:  # type: ignore
            pass


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
        self._encode_kwargs: Dict[str, Any] = kwargs.pop("encode_kwargs", {})
        self._model_kwargs: Dict[str, Any] = kwargs

        self._is_langchain: bool = False
        self._is_st: bool = False

        self._model_name: Optional[str] = None
        self._model: Any = None

        if isinstance(embedding_model, BaseEmbeddings):
            self._model = embedding_model
            self._is_langchain = True
            self._model_name = getattr(embedding_model, "model", None) or getattr(
                embedding_model, "model_name", None) or embedding_model.__class__.__name__
        elif isinstance(embedding_model, str):
            try:
                from sentence_transformers import SentenceTransformer  # type: ignore
            except Exception as exc:
                raise ImportError(
                    "sentence_transformers is required when embedding_model is a string.") from exc
            self._model = SentenceTransformer(
                embedding_model, **self._model_kwargs)
            self._is_st = True
            self._model_name = embedding_model
        else:
            # Fallback: try to use a callable with encode or __call__
            if hasattr(embedding_model, "encode") or callable(embedding_model):
                self._model = embedding_model
                self._model_name = getattr(embedding_model, "name", None) if isinstance(getattr(
                    embedding_model, "name", None), str) else embedding_model.__class__.__name__
            else:
                raise TypeError(
                    "embedding_model must be a string model name, a LangChain Embeddings instance, or an object with an 'encode' method.")

    def name(self) -> str:
        '''Return the name of the embedding model for ChromaDB compatibility.'''
        return str(self._model_name or self.__class__.__name__)

    def __call__(self, input: Union[str, List[str]]) -> Union['np.ndarray', List['np.ndarray']]:
        if isinstance(input, str):
            if self._is_langchain:
                if hasattr(self._model, "embed_query"):
                    # type: ignore[attr-defined]
                    vec = self._model.embed_query(input)
                elif hasattr(self._model, "embed_documents"):
                    vecs = self._model.embed_documents(
                        [input])  # type: ignore[attr-defined]
                    vec = vecs[0] if vecs else []
                else:
                    raise AttributeError(
                        "Provided LangChain embeddings model lacks 'embed_query'/'embed_documents'.")
                return np.asarray(vec, dtype=np.float32)

            if self._is_st:
                return self._model.encode(input, convert_to_numpy=True, **self._encode_kwargs)

            if hasattr(self._model, "encode"):
                return np.asarray(self._model.encode(input, **self._encode_kwargs), dtype=np.float32)
            if callable(self._model):
                return np.asarray(self._model(input, **self._encode_kwargs), dtype=np.float32)
            raise TypeError(
                "Unsupported embedding model interface for single string input.")

        # List[str]
        if not input:
            return []

        if self._is_langchain:
            if hasattr(self._model, "embed_documents"):
                vecs = self._model.embed_documents(
                    input)  # type: ignore[attr-defined]
            elif hasattr(self._model, "embed_query"):
                # type: ignore[attr-defined]
                vecs = [self._model.embed_query(q) for q in input]
            else:
                raise AttributeError(
                    "Provided LangChain embeddings model lacks 'embed_documents'/'embed_query'.")
            return [np.asarray(v, dtype=np.float32) for v in vecs]

        if self._is_st:
            arr = self._model.encode(
                input, convert_to_numpy=True, **self._encode_kwargs)
            if isinstance(arr, np.ndarray):
                return [np.asarray(v, dtype=np.float32) for v in arr]
            return [np.asarray(v, dtype=np.float32) for v in list(arr)]

        if hasattr(self._model, "encode"):
            vecs = self._model.encode(input, **self._encode_kwargs)
            if isinstance(vecs, np.ndarray):
                return [np.asarray(v, dtype=np.float32) for v in vecs]
            return [np.asarray(v, dtype=np.float32) for v in vecs]

        if callable(self._model):
            vecs = [self._model(x, **self._encode_kwargs) for x in input]
            return [np.asarray(v, dtype=np.float32) for v in vecs]

        raise TypeError(
            "Unsupported embedding model interface for list input.")
