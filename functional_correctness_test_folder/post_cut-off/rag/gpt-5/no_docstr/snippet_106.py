from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple, Union

import numpy as np

try:
    # LangChain v0.2+ style
    from langchain_core.embeddings import Embeddings as BaseEmbeddings  # type: ignore
except Exception:
    try:
        # LangChain v0.1 style
        from langchain.embeddings.base import Embeddings as BaseEmbeddings  # type: ignore
    except Exception:
        class BaseEmbeddings(Protocol):
            def embed_documents(self, texts: List[str]) -> List[List[float]]:
                ...

            def embed_query(self, text: str) -> List[float]:
                ...


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
        self._encoder: Callable[[List[str]], np.ndarray]
        self._name: str = "unknown"
        self._model_obj: Any = None
        self._encode_kwargs: Dict[str, Any] = {}
        self._init_kwargs: Dict[str, Any] = dict(kwargs) if kwargs else {}

        # If provided a LangChain-like embeddings object
        if hasattr(embedding_model, "embed_documents") or hasattr(embedding_model, "embed_query"):
            self._model_obj = embedding_model
            self._name = getattr(embedding_model, "model_name", None) or getattr(
                embedding_model, "model", None) or embedding_model.__class__.__name__

            def _encode_langchain(texts: List[str]) -> np.ndarray:
                vectors = embedding_model.embed_documents(
                    texts)  # type: ignore[attr-defined]
                return np.asarray(vectors, dtype=np.float32)

            self._encoder = _encode_langchain
            return

        # If provided a string identifier, try to load a SentenceTransformer
        if isinstance(embedding_model, str):
            self._name = embedding_model

            # Attempt sentence-transformers first
            try:
                from sentence_transformers import SentenceTransformer  # type: ignore

                st_model = SentenceTransformer(
                    embedding_model, **self._init_kwargs)
                self._model_obj = st_model

                def _encode_st(texts: List[str]) -> np.ndarray:
                    # convert_to_numpy ensures np.ndarray output
                    return st_model.encode(
                        texts,
                        convert_to_numpy=True,
                        normalize_embeddings=self._init_kwargs.get(
                            "normalize_embeddings", True),
                        batch_size=self._init_kwargs.get("batch_size", 32),
                        show_progress_bar=self._init_kwargs.get(
                            "show_progress_bar", False),
                    ).astype(np.float32)

                self._encoder = _encode_st
                return
            except Exception:
                pass

            # Fallback: HuggingFace transformers mean pooling
            try:
                import torch
                from transformers import AutoModel, AutoTokenizer  # type: ignore

                tok = AutoTokenizer.from_pretrained(
                    embedding_model, **self._init_kwargs)
                mdl = AutoModel.from_pretrained(
                    embedding_model, **self._init_kwargs)
                mdl.eval()
                self._model_obj = mdl

                device: Union[str, torch.device] = self._init_kwargs.get(
                    "device", "cpu")
                mdl.to(device)

                def _mean_pool(last_hidden_state: "torch.Tensor", attention_mask: "torch.Tensor") -> "torch.Tensor":
                    mask = attention_mask.unsqueeze(
                        -1).type_as(last_hidden_state)
                    masked = last_hidden_state * mask
                    summed = masked.sum(dim=1)
                    counts = mask.sum(dim=1).clamp(min=1)
                    return summed / counts

                def _encode_hf(texts: List[str]) -> np.ndarray:
                    if len(texts) == 0:
                        return np.empty((0, 0), dtype=np.float32)
                    with torch.no_grad():
                        inputs = tok(
                            texts,
                            padding=True,
                            truncation=True,
                            return_tensors="pt",
                            max_length=self._init_kwargs.get(
                                "max_length", 512),
                        )
                        inputs = {k: v.to(device) for k, v in inputs.items()}
                        outputs = mdl(**inputs)
                        pooled = _mean_pool(
                            outputs.last_hidden_state, inputs["attention_mask"])
                        if self._init_kwargs.get("normalize_embeddings", True):
                            pooled = torch.nn.functional.normalize(
                                pooled, p=2, dim=1)
                        return pooled.detach().cpu().numpy().astype(np.float32)

                self._encoder = _encode_hf
                return
            except Exception:
                pass

            # As last resort, if user passes a callable factory in kwargs to build encoder
            encoder = self._init_kwargs.get("encoder")
            if callable(encoder):
                self._encoder = lambda texts: np.asarray(
                    encoder(texts), dtype=np.float32)
                return

            raise RuntimeError(
                f"Unable to initialize embedding model from identifier '{embedding_model}'. "
                "Tried: sentence-transformers and transformers backends. "
                "Please install the required dependencies or pass a pre-initialized embeddings object."
            )

        # If provided a generic object with an 'encode' method
        if hasattr(embedding_model, "encode"):
            self._model_obj = embedding_model
            self._name = getattr(embedding_model, "model_name", None) or getattr(
                embedding_model, "name", None) or embedding_model.__class__.__name__

            def _encode_generic(texts: List[str]) -> np.ndarray:
                # type: ignore[attr-defined]
                vecs = embedding_model.encode(texts, **self._init_kwargs)
                return np.asarray(vecs, dtype=np.float32)

            self._encoder = _encode_generic
            return

        raise TypeError(
            "embedding_model must be either a string model identifier, a LangChain-like Embeddings instance, "
            "or an object exposing an 'encode' method."
        )

    def name(self) -> str:
        '''Return the name of the embedding model for ChromaDB compatibility.'''
        return self._name

    def __call__(self, input: Union[str, List[str]]) -> Union['np.ndarray', List['np.ndarray']]:
        '''Call the ChromaEmbeddingFunction.'''
        if isinstance(input, str):
            arr = self._encoder([input])
            if arr.ndim == 2 and arr.shape[0] == 1:
                return arr[0]
            return np.asarray(arr).reshape(-1)
        elif isinstance(input, list):
            if not all(isinstance(x, str) for x in input):
                raise TypeError("All elements of input list must be strings.")
            return self._encoder(input)
        else:
            raise TypeError("Input must be a string or a list of strings.")
