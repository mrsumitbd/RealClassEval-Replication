from typing import Any, Dict, List, Union, Optional

try:
    import numpy as np
except Exception:  # pragma: no cover
    np = None  # type: ignore

# Try to import a BaseEmbeddings interface from LangChain, provide a minimal fallback otherwise
try:
    from langchain_core.embeddings import Embeddings as BaseEmbeddings  # type: ignore
except Exception:
    try:
        from langchain.embeddings.base import Embeddings as BaseEmbeddings  # type: ignore
    except Exception:
        class BaseEmbeddings:  # type: ignore
            def embed_documents(self, texts: List[str]) -> List[List[float]]:
                raise NotImplementedError

            def embed_query(self, text: str) -> List[float]:
                raise NotImplementedError


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
        self._st_model = None  # SentenceTransformer instance or None
        self._lc_embedder: Optional[BaseEmbeddings] = None
        self._model_name: str

        # Normalization flag
        self._normalize: bool = bool(
            kwargs.pop('normalize', kwargs.pop('normalize_embeddings', False))
        )

        # Optional encode kwargs (only applicable to SentenceTransformer)
        self._encode_kwargs: Dict[str, Any] = {}
        for k in ('batch_size', 'show_progress_bar'):
            if k in kwargs:
                self._encode_kwargs[k] = kwargs.pop(k)

        if isinstance(embedding_model, str):
            try:
                from sentence_transformers import SentenceTransformer
            except Exception as e:  # pragma: no cover
                raise ImportError(
                    "sentence-transformers is required to load embedding model by name. "
                    "Install via `pip install sentence-transformers` or pass a LangChain BaseEmbeddings instance."
                ) from e

            device = kwargs.pop('device', None)
            st_init_kwargs: Dict[str, Any] = {}
            if device is not None:
                st_init_kwargs['device'] = device
            # Remaining kwargs (if any) are passed to the model constructor
            st_init_kwargs.update(kwargs)

            self._st_model = SentenceTransformer(
                embedding_model, **st_init_kwargs)
            self._model_name = embedding_model
        else:
            # A LangChain embeddings instance
            self._lc_embedder = embedding_model
            # Try to get a meaningful name if available
            self._model_name = getattr(embedding_model, 'model', None) or getattr(
                embedding_model, 'model_name', None
            ) or embedding_model.__class__.__name__

    def name(self) -> str:
        '''Return the name of the embedding model for ChromaDB compatibility.'''
        return self._model_name

    def __call__(self, input: Union[str, List[str]]) -> Union['np.ndarray', List['np.ndarray']]:
        '''Call the ChromaEmbeddingFunction.'''
        if np is None:  # pragma: no cover
            raise ImportError("numpy is required for ChromaEmbeddingFunction")

        single_input = isinstance(input, str)
        texts: List[str] = [input] if single_input else list(input)

        if self._st_model is not None:
            # SentenceTransformers path
            embs = self._st_model.encode(
                texts,
                convert_to_numpy=True,
                normalize_embeddings=self._normalize,
                **self._encode_kwargs,
            )
            arr = np.asarray(embs)
        elif self._lc_embedder is not None:
            # LangChain BaseEmbeddings path
            if hasattr(self._lc_embedder, 'embed_documents'):
                embs = self._lc_embedder.embed_documents(
                    texts)  # type: ignore[attr-defined]
            else:
                # type: ignore[attr-defined]
                embs = [self._lc_embedder.embed_query(t) for t in texts]

            arr = np.asarray(embs, dtype=np.float32)

            if self._normalize:
                if arr.ndim == 2:
                    norms = np.linalg.norm(arr, axis=1, keepdims=True)
                    norms = np.where(norms == 0, 1.0, norms)
                    arr = arr / norms
                elif arr.ndim == 1:
                    n = np.linalg.norm(arr)
                    arr = arr / (n if n != 0 else 1.0)
        else:  # pragma: no cover
            raise RuntimeError("No embedding model is initialized.")

        if single_input:
            return arr[0]
        return arr.tolist() if isinstance(arr, list) else arr
