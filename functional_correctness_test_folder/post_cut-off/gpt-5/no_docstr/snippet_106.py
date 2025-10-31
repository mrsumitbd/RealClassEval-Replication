from typing import Any, Dict, List, Union

import numpy as np

try:
    from langchain.embeddings.base import Embeddings as BaseEmbeddings  # type: ignore
except Exception:
    try:
        from llama_index.core.base.embeddings.base import BaseEmbedding as BaseEmbeddings  # type: ignore
    except Exception:
        from typing import Protocol

        class BaseEmbeddings(Protocol):  # type: ignore
            def embed_documents(self, texts: List[str]) -> List[List[float]]:
                ...

            def embed_query(self, text: str) -> List[float]:
                ...


class ChromaEmbeddingFunction:
    def __init__(self, embedding_model: Union[str, BaseEmbeddings] = 'minishlab/potion-retrieval-32M', **kwargs: Dict[str, Any]) -> None:
        self._backend: str = "unknown"
        self._model_name: str = ""
        self._kwargs: Dict[str, Any] = dict(kwargs)
        self._normalize = bool(self._kwargs.pop("normalize_embeddings", False))

        if isinstance(embedding_model, str):
            self._model_name = embedding_model
            try:
                from sentence_transformers import SentenceTransformer  # type: ignore
            except Exception as e:
                raise ImportError(
                    "sentence-transformers is required when embedding_model is a string. "
                    "Install via `pip install sentence-transformers`."
                ) from e
            self._model = SentenceTransformer(self._model_name, **self._kwargs)
            self._backend = "sentence_transformers"
        else:
            # Treat as a provided embeddings implementation (e.g., LangChain, LlamaIndex)
            self._model = embedding_model
            # Try to capture a readable name
            name = getattr(embedding_model, "model_name", None) or getattr(
                embedding_model, "name", None)
            if callable(name):
                try:
                    name = name()
                except Exception:
                    name = None
            if not isinstance(name, str) or not name:
                name = getattr(embedding_model, "__class__",
                               type(embedding_model)).__name__
            self._model_name = str(name)
            # Identify available interface
            if hasattr(embedding_model, "embed_documents") and hasattr(embedding_model, "embed_query"):
                self._backend = "base_embeddings"
            elif hasattr(embedding_model, "encode"):
                self._backend = "encode_like"
            else:
                self._backend = "callable_like"

    def name(self) -> str:
        if self._backend == "sentence_transformers":
            return f"sentence-transformers:{self._model_name}"
        return str(self._model_name or "embedding_model")

    def __call__(self, input: Union[str, List[str]]) -> Union['np.ndarray', List['np.ndarray']]:
        # sentence-transformers backend
        if self._backend == "sentence_transformers":
            if isinstance(input, str):
                vecs = self._model.encode(
                    [input], convert_to_numpy=True, normalize_embeddings=self._normalize)
                return np.asarray(vecs[0])
            else:
                vecs = self._model.encode(
                    input, convert_to_numpy=True, normalize_embeddings=self._normalize)
                vecs = np.asarray(vecs)
                return [np.asarray(v) for v in vecs]

        # BaseEmbeddings-like backend
        if self._backend == "base_embeddings":
            if isinstance(input, str):
                # type: ignore[attr-defined]
                v = self._model.embed_query(input)
                return np.asarray(v, dtype=float)
            else:
                vs = self._model.embed_documents(
                    input)  # type: ignore[attr-defined]
                return [np.asarray(v, dtype=float) for v in vs]

        # encode-like backend (e.g., custom models exposing encode)
        if self._backend == "encode_like" and hasattr(self._model, "encode"):
            if isinstance(input, str):
                # type: ignore[attr-defined]
                vecs = self._model.encode([input])
                vecs = np.asarray(vecs)
                return np.asarray(vecs[0], dtype=float)
            else:
                vecs = self._model.encode(input)  # type: ignore[attr-defined]
                vecs = np.asarray(vecs)
                return [np.asarray(v, dtype=float) for v in vecs]

        # callable-like fallback
        if isinstance(input, str):
            out = self._model(input)  # type: ignore[misc]
            return np.asarray(out, dtype=float)
        else:
            out = self._model(input)  # type: ignore[misc]
            arr = np.asarray(out)
            if arr.ndim == 2:
                return [np.asarray(v, dtype=float) for v in arr]
            # type: ignore[iteration-over-optional]
            return [np.asarray(v, dtype=float) for v in out]
