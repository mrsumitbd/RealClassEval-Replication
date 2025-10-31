"""
Retrieval logic for finding similar class skeletons.
"""

import json
from typing import List, Dict, Any
from dataclasses import dataclass
from pathlib import Path
import logging

from rag_config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class RetrievedExample:
    """A retrieved example with skeleton and implementation."""
    class_name: str
    skeleton: str
    implementation: str
    similarity_score: float
    index: int
    metadata: Dict[str, Any] = None


class DatasetRetriever:
    """Retrieve examples from v1 dataset based on similarity."""

    def __init__(self, v1_dataset_path: str = None):
        """
        Initialize retriever with v1 dataset.

        Args:
            v1_dataset_path: Path to v1 dataset JSON file
        """
        self.dataset_path = v1_dataset_path or Config.V1_DATASET_PATH
        self.v1_data = []
        self._load_dataset()

    def _load_dataset(self):
        """Load v1 dataset from JSON."""
        logger.info(f"Loading v1 dataset from {self.dataset_path}")

        with open(self.dataset_path, 'r') as f:
            data = json.load(f)

        # Convert to list of dictionaries
        if isinstance(data, list):
            self.v1_data = data
        else:
            raise ValueError("Dataset should be a list of examples")

        logger.info(f"Loaded {len(self.v1_data)} examples from v1 dataset")

    def retrieve_by_indices(self, indices: List[int], distances: List[float]) -> List[RetrievedExample]:
        """
        Retrieve examples by their indices in the dataset.

        Args:
            indices: List of indices from FAISS search
            distances: List of distances from FAISS search

        Returns:
            List of RetrievedExample objects
        """
        examples = []

        for idx, distance in zip(indices, distances):
            if idx >= len(self.v1_data):
                logger.warning(f"Index {idx} out of bounds, skipping")
                continue

            data_point = self.v1_data[idx]

            # Convert distance to similarity score
            similarity_score = 1 / (1 + distance)

            example = RetrievedExample(
                class_name=data_point.get('class_name', 'Unknown'),
                skeleton=data_point.get('skeleton', ''),
                implementation=data_point.get('implementation', ''),
                similarity_score=similarity_score,
                index=idx,
                metadata=data_point.get('metadata', {})
            )

            examples.append(example)

        logger.info(f"Retrieved {len(examples)} examples")
        return examples

    def get_example_by_index(self, index: int) -> Dict[str, Any]:
        """Get a single example by index."""
        if index >= len(self.v1_data):
            raise IndexError(f"Index {index} out of bounds")
        return self.v1_data[index]

    def get_dataset_size(self) -> int:
        """Get size of v1 dataset."""
        return len(self.v1_data)


class RAGRetriever:
    """Main retriever combining index search and dataset lookup."""

    def __init__(self, index_builder, dataset_retriever, use_metric_filtering: bool = False):
        """
        Initialize RAG retriever.

        Args:
            index_builder: IndexBuilder instance
            dataset_retriever: DatasetRetriever instance
            use_metric_filtering: Whether to use metrics for filtering (optional)
        """
        self.index_builder = index_builder
        self.dataset_retriever = dataset_retriever
        self.use_metric_filtering = use_metric_filtering

    def retrieve(self, query_skeleton: str, k: int = None,
                 target_metrics: dict = None) -> List[RetrievedExample]:
        """
        Retrieve k most similar examples for a query skeleton.

        Args:
            query_skeleton: Target skeleton from v2
            k: Number of examples to retrieve
            target_metrics: Optional dict of target metrics for filtering

        Returns:
            List of RetrievedExample objects
        """
        k = k or Config.TOP_K_EXAMPLES

        logger.info(f"Retrieving {k} similar examples")

        # Step 1: Search in FAISS index (get more if filtering)
        search_k = k * 3 if self.use_metric_filtering and target_metrics else k
        distances, indices = self.index_builder.search(query_skeleton, k=search_k)

        # Step 2: Retrieve full examples from dataset
        examples = self.dataset_retriever.retrieve_by_indices(indices, distances)

        # Step 3: Optional metric-based filtering
        if self.use_metric_filtering and target_metrics:
            examples = self._filter_by_metrics(examples, target_metrics)

        # Return top k after filtering
        return examples[:k]

    def _filter_by_metrics(self, examples: List[RetrievedExample],
                           target_metrics: dict) -> List[RetrievedExample]:
        """
        Filter examples based on metric similarity.

        Args:
            examples: List of retrieved examples
            target_metrics: Target metrics to match against

        Returns:
            Filtered and re-ranked examples
        """
        if not examples:
            return examples

        filtered = []

        for example in examples:
            if not example.metadata or 'understand_metrics' not in example.metadata:
                # No metrics available, keep example but with lower priority
                filtered.append((example, 0))
                continue

            example_metrics = example.metadata['understand_metrics']
            score = self._calculate_metric_similarity(target_metrics, example_metrics)

            # Only keep if similarity is reasonable
            if score > 0:
                filtered.append((example, score))

        # Sort by metric similarity (higher is better)
        filtered.sort(key=lambda x: x[1], reverse=True)

        logger.info(f"Filtered {len(examples)} -> {len(filtered)} examples using metrics")

        return [ex for ex, score in filtered]

    def _calculate_metric_similarity(self, target: dict, example: dict) -> float:
        """
        Calculate similarity score based on metrics.

        Args:
            target: Target metrics
            example: Example metrics

        Returns:
            Similarity score (0-1, higher is better)
        """
        score = 0.0
        count = 0

        # Check key metrics with tolerance
        for metric, tolerance in Config.METRIC_TOLERANCE.items():
            if metric in target and metric in example:
                target_val = target[metric]
                example_val = example[metric]

                # Calculate normalized difference
                diff = abs(target_val - example_val)
                if diff <= tolerance:
                    # Within tolerance - score based on how close
                    metric_score = 1.0 - (diff / tolerance)
                    score += metric_score
                    count += 1

        # Return average score
        return score / count if count > 0 else 0.0

    def retrieve_with_filter(self, query_skeleton: str, k: int = None,
                             filter_func=None) -> List[RetrievedExample]:
        """
        Retrieve examples with custom filtering function.

        Args:
            query_skeleton: Target skeleton from v2
            k: Number of examples to retrieve
            filter_func: Optional function to filter examples

        Returns:
            List of filtered RetrievedExample objects
        """
        # Retrieve more examples than needed
        extra_k = k * 3 if k else Config.TOP_K_EXAMPLES * 3
        examples = self.retrieve(query_skeleton, k=extra_k)

        # Apply filter if provided
        if filter_func:
            examples = [ex for ex in examples if filter_func(ex)]

        # Return top k after filtering
        return examples[:k or Config.TOP_K_EXAMPLES]


def main():
    """Test the retriever."""
    from rag_embedder import CodeEmbedder
    from rag_indexer import IndexBuilder

    # Create test dataset
    test_data = [
        {
            "class_name": "UserManager",
            "skeleton": "class UserManager:\n    def create(self): ...",
            "implementation": "class UserManager:\n    def create(self):\n        return True",
            "metadata": {"domain": "database"}
        },
        {
            "class_name": "DataProcessor",
            "skeleton": "class DataProcessor:\n    async def process(self): ...",
            "implementation": "class DataProcessor:\n    async def process(self):\n        return []",
            "metadata": {"domain": "async"}
        }
    ]

    # Save test dataset
    test_path = "test_v1_dataset.json"
    with open(test_path, 'w') as f:
        json.dump(test_data, f)

    # Initialize components
    embedder = CodeEmbedder()
    index_builder = IndexBuilder(embedder)

    # Build index
    skeletons = [d['skeleton'] for d in test_data]
    index_builder.build_from_skeletons(skeletons, save=False)

    # Initialize retriever
    dataset_retriever = DatasetRetriever(test_path)
    rag_retriever = RAGRetriever(index_builder, dataset_retriever)

    # Test retrieval
    query = "class AsyncHandler:\n    async def handle(self): ..."
    print(f"Query: {query}")

    examples = rag_retriever.retrieve(query, k=2)

    print(f"\nRetrieved {len(examples)} examples:")
    for i, ex in enumerate(examples, 1):
        print(f"\n{i}. {ex.class_name} (similarity: {ex.similarity_score:.3f})")
        print(f"   Skeleton: {ex.skeleton[:50]}...")
        print(f"   Implementation: {ex.implementation[:50]}...")

    # Cleanup
    Path(test_path).unlink()


if __name__ == "__main__":
    main()