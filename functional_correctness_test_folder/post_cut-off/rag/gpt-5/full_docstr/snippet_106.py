import numpy as np
from typing import Any, Dict, List, Optional, Protocol, Union, runtime_checkable, Callable


@runtime_checkable
class BaseEmbeddings(Protocol):
    def embed_documents(self, texts: List[str]) -> List[List[float]]: ...
    def embed_query(self, text: str) -> List[float]: ...


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
        self._normalize: bool = bool(kwargs.pop("normalize", False))
        self._model: Union[Any, Callable[..., Any]]
        self._model_name: str

        if isinstance(embedding_model, str):
            self._model_name = embedding_model
            # Try sentence-transformers first
            st_model: Optional[Any] = None
            try:
                from sentence_transformers import SentenceTransformer  # type: ignore
                st_model = SentenceTransformer(embedding_model, **kwargs)
            except Exception as e:
                st_model = None
            if st_model is not None:
                self._model = st_model
            else:
                # Fallback to transformers feature-extraction pipeline
                try:
                    from transformers import AutoTokenizer, AutoModel  # type: ignore
                    import torch  # type: ignore

                    class _HFEncoder:
                        def __init__(self, name: str, init_kwargs: Dict[str, Any]):
                            self.tokenizer = AutoTokenizer.from_pretrained(
                                name, **{k: v for k, v in init_kwargs.items() if k != "device"})
                            self.model = AutoModel.from_pretrained(
                                name, **{k: v for k, v in init_kwargs.items() if k != "device"})
                            self.device = init_kwargs.get("device", "cpu")
                            if self.device and hasattr(self.model, "to"):
                                self.model = self.model.to(self.device)

                        @torch.inference_mode()
                        def encode(self, texts: List[str], **encode_kwargs: Any):
                            from torch.nn.functional import normalize as torch_norm  # type: ignore

                            batch = self.tokenizer(
                                texts,
                                padding=True,
                                truncation=True,
                                return_tensors="pt",
                                max_length=encode_kwargs.get(
                                    "max_length", 512),
                            )
                            batch = {k: v.to(self.model.device)
                                     for k, v in batch.items()}
                            outputs = self.model(**batch)
                            # Mean Pooling over token embeddings with attention mask
                            # (bs, seq, hid)
                            token_embeds = outputs.last_hidden_state
                            # (bs, seq, 1)
                            attn_mask = batch["attention_mask"].unsqueeze(-1)
                            summed = (token_embeds * attn_mask).sum(dim=1)
                            counts = attn_mask.sum(dim=1).clamp(min=1)
                            embeds = summed / counts
                            if encode_kwargs.get("normalize_embeddings", False):
                                embeds = torch_norm(embeds, p=2, dim=1)
                            return embeds.detach().cpu().numpy()

                    self._model = _HFEncoder(embedding_model, kwargs)
                except Exception as err:
                    raise RuntimeError(
                        f"Unable to initialize embedding model '{embedding_model}'. "
                        f"Install 'sentence-transformers' or 'transformers', or pass a model object."
                    ) from err
        else:
            self._model = embedding_model
            # Best-effort name extraction
            name = (
                getattr(embedding_model, "model_name", None)
                or getattr(embedding_model, "model_id", None)
                or getattr(embedding_model, "name", None)
            )
            self._model_name = str(name) if name else type(
                embedding_model).__name__

    def name(self) -> str:
        '''Return the name of the embedding model for ChromaDB compatibility.'''
        return self._model_name

    def __call__(self, input: Union[str, List[str]]) -> Union['np.ndarray', List['np.ndarray']]:
        '''Call the ChromaEmbeddingFunction.'''
        if isinstance(input, str):
            texts = [input]
            is_single = True
        elif isinstance(input, list) and all(isinstance(t, str) for t in input):
            texts = input
            is_single = False
        else:
            raise TypeError("input must be a string or a list of strings")

        vectors = self._embed_texts(texts)

        if self._normalize:
            normalized = []
            for v in vectors:
                norm = float(np.linalg.norm(v))
                if norm == 0.0:
                    normalized.append(v)
                else:
                    normalized.append(v / norm)
            vectors = normalized

        if is_single:
            return vectors[0] if vectors else np.zeros((0,), dtype=np.float32)
        return vectors

    def _embed_texts(self, texts: List[str]) -> List[np.ndarray]:
        model = self._model

        # sentence-transformers-like
        if hasattr(model, "encode"):
            result = model.encode(texts, **self._encode_kwargs)
            return self._to_list_of_arrays(result)

        # langchain embeddings-like
        has_docs = hasattr(model, "embed_documents")
        has_query = hasattr(model, "embed_query")
        if has_docs or has_query:
            try:
                if has_docs:
                    # type: ignore[attr-defined]
                    result = model.embed_documents(texts)
                else:
                    # type: ignore[attr-defined]
                    result = [model.embed_query(t) for t in texts]
                return self._to_list_of_arrays(result)
            except Exception as e:
                raise RuntimeError(
                    "Failed to generate embeddings using provided embeddings object.") from e

        # Callable model
        if callable(model):
            result = model(texts)
            return self._to_list_of_arrays(result)

        raise TypeError(
            "Unsupported embedding model type. Provide a model with 'encode', 'embed_documents/embed_query', or a callable.")

    @staticmethod
    def _to_list_of_arrays(result: Any) -> List[np.ndarray]:
        if isinstance(result, np.ndarray):
            if result.ndim == 1:
                return [result.astype(np.float32, copy=False)]
            elif result.ndim == 2:
                return [row.astype(np.float32, copy=False) for row in result]
            else:
                raise ValueError("Embedding output ndarray must be 1D or 2D.")
        if isinstance(result, (list, tuple)):
            if len(result) == 0:
                return []
            first = result[0]
            # If nested lists (list of vectors)
            if isinstance(first, (list, tuple, np.ndarray)):
                # type: ignore[arg-type]
                return [np.asarray(vec, dtype=np.float32) for vec in result]
            # If flat list for a single vector
            if isinstance(first, (float, int)):
                # type: ignore[arg-type]
                return [np.asarray(result, dtype=np.float32)]
        raise ValueError("Unsupported embedding output format.")
