"""
FAISS index creation and management for vector similarity search.
"""

import faiss
import numpy as np
from pathlib import Path
import logging

from rag_config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FAISSIndexer:
    """Manage FAISS index for fast similarity search."""

    def __init__(self, dimension: int):
        """
        Initialize FAISS indexer.

        Args:
            dimension: Dimension of embeddings
        """
        self.dimension = dimension
        self.index = None
        logger.info(f"Initialized FAISS indexer with dimension {dimension}")

    def create_index(self, embeddings: np.ndarray, metric: str = None):
        """
        Create FAISS index from embeddings.

        Args:
            embeddings: Numpy array of embeddings (n_samples, dimension)
            metric: Similarity metric ('l2' or 'cosine')
        """
        metric = metric or Config.SIMILARITY_METRIC

        logger.info(f"Creating FAISS index with {len(embeddings)} embeddings")
        logger.info(f"Metric: {metric}")

        # Ensure embeddings are float32
        embeddings = embeddings.astype('float32')

        # Create index based on metric
        if metric == "l2":
            self.index = faiss.IndexFlatL2(self.dimension)
        elif metric == "cosine":
            # For cosine similarity, normalize vectors and use L2
            faiss.normalize_L2(embeddings)
            self.index = faiss.IndexFlatL2(self.dimension)
        else:
            raise ValueError(f"Unknown metric: {metric}")

        # Add embeddings to index
        self.index.add(embeddings)

        logger.info(f"Index created with {self.index.ntotal} vectors")

    def search(self, query_embedding: np.ndarray, k: int = None) -> tuple:
        """
        Search for k nearest neighbors.

        Args:
            query_embedding: Query embedding (1, dimension) or (dimension,)
            k: Number of neighbors to retrieve

        Returns:
            Tuple of (distances, indices)
        """
        if self.index is None:
            raise ValueError("Index not created. Call create_index() first.")

        k = k or Config.TOP_K_EXAMPLES

        # Ensure query is 2D and float32
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        query_embedding = query_embedding.astype('float32')

        # Search
        distances, indices = self.index.search(query_embedding, k)

        return distances[0], indices[0]

    def save(self, path: str = None):
        """
        Save FAISS index to disk.

        Args:
            path: Path to save index (default from config)
        """
        if self.index is None:
            raise ValueError("Index not created. Nothing to save.")

        path = path or Config.INDEX_SAVE_PATH
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        faiss.write_index(self.index, str(path))
        logger.info(f"Index saved to {path}")

    def load(self, path: str = None):
        """
        Load FAISS index from disk.

        Args:
            path: Path to load index from (default from config)
        """
        path = path or Config.INDEX_SAVE_PATH
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"Index file not found: {path}")

        self.index = faiss.read_index(str(path))
        logger.info(f"Index loaded from {path}")
        logger.info(f"Index contains {self.index.ntotal} vectors")

    def get_index_size(self) -> int:
        """Get number of vectors in index."""
        if self.index is None:
            return 0
        return self.index.ntotal


class IndexBuilder:
    """Build and manage FAISS index for v1 dataset."""

    def __init__(self, embedder):
        """
        Initialize index builder.

        Args:
            embedder: CodeEmbedder instance
        """
        self.embedder = embedder
        self.dimension = embedder.get_embedding_dimension()
        self.indexer = FAISSIndexer(self.dimension)

    def build_from_skeletons(self, skeletons: list, save: bool = True):
        """
        Build index from list of code skeletons.

        Args:
            skeletons: List of code skeleton strings
            save: Whether to save index and embeddings to disk
        """
        logger.info(f"Building index from {len(skeletons)} skeletons")

        # Generate embeddings
        logger.info("Generating embeddings...")
        embeddings = self.embedder.embed_batch(skeletons, show_progress=True)

        # Create index
        logger.info("Creating FAISS index...")
        self.indexer.create_index(embeddings)

        # Save if requested
        if save:
            self.save_index_and_embeddings(embeddings)

        return embeddings

    def save_index_and_embeddings(self, embeddings: np.ndarray):
        """Save both index and embeddings."""
        # Save FAISS index
        self.indexer.save()

        # Save embeddings
        embeddings_path = Path(Config.EMBEDDINGS_SAVE_PATH)
        embeddings_path.parent.mkdir(parents=True, exist_ok=True)
        np.save(embeddings_path, embeddings)
        logger.info(f"Embeddings saved to {embeddings_path}")

    def load_index(self):
        """Load existing index from disk."""
        self.indexer.load()

    def search(self, query_skeleton: str, k: int = None) -> tuple:
        """
        Search for similar skeletons.

        Args:
            query_skeleton: Query code skeleton
            k: Number of results to return

        Returns:
            Tuple of (distances, indices)
        """
        # Generate query embedding
        query_embedding = self.embedder.embed_single(query_skeleton)

        # Search
        return self.indexer.search(query_embedding, k)


def main():
    """Test the indexer."""
    from rag_embedder import CodeEmbedder

    # Create dummy data
    skeletons = [
        "class Example1:\n    def method(self): ...",
        "class Example2:\n    def process(self): ...",
        "class Example3:\n    async def fetch(self): ...",
    ]

    # Initialize
    embedder = CodeEmbedder()
    builder = IndexBuilder(embedder)

    # Build index
    print("Building index...")
    embeddings = builder.build_from_skeletons(skeletons, save=False)
    print(f"Built index with {len(embeddings)} embeddings")

    # Test search
    query = "class Test:\n    async def get_data(self): ..."
    print(f"\nSearching for similar to: {query}")
    distances, indices = builder.search(query, k=2)

    print("\nResults:")
    for i, (dist, idx) in enumerate(zip(distances, indices)):
        print(f"{i + 1}. Index {idx}, Distance: {dist:.3f}")
        print(f"   {skeletons[idx][:50]}...")


if __name__ == "__main__":
    main()