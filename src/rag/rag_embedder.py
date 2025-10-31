"""
Code embedding generation using CodeBERT.
"""

import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel
from typing import List, Union
from tqdm import tqdm
import logging

from rag_config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CodeEmbedder:
    """Generate embeddings for code snippets using CodeBERT."""

    def __init__(self, model_name: str = None, device: str = None):
        """
        Initialize CodeBERT embedder.

        Args:
            model_name: Hugging Face model name (default from config)
            device: Device to use ('cpu' or 'cuda')
        """
        self.model_name = model_name or Config.EMBEDDING_MODEL
        self.device = device or Config.DEVICE

        logger.info(f"Loading model: {self.model_name}")
        logger.info(f"Using device: {self.device}")

        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)
        self.model.to(self.device)
        self.model.eval()

        logger.info("Model loaded successfully")

    def embed_single(self, code: str) -> np.ndarray:
        """
        Generate embedding for a single code snippet.

        Args:
            code: Code snippet as string

        Returns:
            Embedding as numpy array
        """
        # Tokenize
        inputs = self.tokenizer(
            code,
            return_tensors="pt",
            max_length=Config.MAX_SEQUENCE_LENGTH,
            truncation=True,
            padding=True
        )

        # Move to device
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        # Generate embedding
        with torch.no_grad():
            outputs = self.model(**inputs)
            # Use CLS token embedding (first token)
            embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy()

        return embedding[0]

    def embed_batch(self, codes: List[str], batch_size: int = None,
                    show_progress: bool = True) -> np.ndarray:
        """
        Generate embeddings for multiple code snippets.

        Args:
            codes: List of code snippets
            batch_size: Batch size for processing (default from config)
            show_progress: Whether to show progress bar

        Returns:
            Numpy array of embeddings with shape (n_codes, embedding_dim)
        """
        batch_size = batch_size or Config.BATCH_SIZE
        embeddings = []

        iterator = range(0, len(codes), batch_size)
        if show_progress:
            iterator = tqdm(iterator, desc="Generating embeddings")

        for i in iterator:
            batch = codes[i:i + batch_size]
            batch_embeddings = self._process_batch(batch)
            embeddings.append(batch_embeddings)

        return np.vstack(embeddings)

    def _process_batch(self, batch: List[str]) -> np.ndarray:
        """Process a batch of code snippets."""
        # Tokenize batch
        inputs = self.tokenizer(
            batch,
            return_tensors="pt",
            max_length=Config.MAX_SEQUENCE_LENGTH,
            truncation=True,
            padding=True
        )

        # Move to device
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        # Generate embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
            # Use CLS token embeddings
            embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()

        return embeddings

    def embed(self, codes: Union[str, List[str]], **kwargs) -> np.ndarray:
        """
        Convenience method to embed single or multiple code snippets.

        Args:
            codes: Single code string or list of code strings
            **kwargs: Additional arguments for embed_batch

        Returns:
            Embedding(s) as numpy array
        """
        if isinstance(codes, str):
            return self.embed_single(codes)
        else:
            return self.embed_batch(codes, **kwargs)

    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings."""
        # Generate a dummy embedding to get dimension
        dummy_code = "def hello(): pass"
        embedding = self.embed_single(dummy_code)
        return embedding.shape[0]


def main():
    """Test the embedder."""
    embedder = CodeEmbedder()

    # Test single embedding
    code = """
class Example:
    def __init__(self):
        pass

    def method(self):
        return True
"""

    print("Testing single embedding...")
    embedding = embedder.embed_single(code)
    print(f"Embedding shape: {embedding.shape}")
    print(f"Embedding dimension: {embedder.get_embedding_dimension()}")

    # Test batch embedding
    codes = [code] * 10
    print("\nTesting batch embedding...")
    embeddings = embedder.embed_batch(codes, show_progress=True)
    print(f"Batch embeddings shape: {embeddings.shape}")


if __name__ == "__main__":
    main()