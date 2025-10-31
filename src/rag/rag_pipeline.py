"""
Main RAG pipeline orchestration.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

from rag_config import Config
from rag_embedder import CodeEmbedder
from rag_indexer import IndexBuilder
from rag_retriever import DatasetRetriever, RAGRetriever
from rag_prompt_builder import PromptBuilder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGPipeline:
    """Complete RAG pipeline for class generation."""

    def __init__(self, v1_dataset_path: str = None, rebuild_index: bool = False, use_metric_filtering: bool = False):
        """
        Initialize RAG pipeline.

        Args:
            v1_dataset_path: Path to v1 dataset
            rebuild_index: Whether to rebuild index from scratch
        """
        Config.create_directories()

        self.v1_dataset_path = v1_dataset_path or Config.V1_DATASET_PATH

        # Initialize components
        logger.info("Initializing RAG pipeline...")
        self.embedder = CodeEmbedder()
        self.index_builder = IndexBuilder(self.embedder)
        self.dataset_retriever = DatasetRetriever(self.v1_dataset_path)
        self.rag_retriever = RAGRetriever(self.index_builder, self.dataset_retriever)
        self.prompt_builder = PromptBuilder()
        self.use_metric_filtering = use_metric_filtering

        # Build or load index
        self._setup_index(rebuild_index)

        logger.info("RAG pipeline initialized successfully")

    def _setup_index(self, rebuild: bool):
        """Setup FAISS index (build or load)."""
        index_path = Path(Config.INDEX_SAVE_PATH)

        if rebuild or not index_path.exists():
            logger.info("Building new index from v1 dataset...")
            self._build_index()
        else:
            logger.info("Loading existing index...")
            self.index_builder.load_index()

    def _build_index(self):
        """Build index from v1 dataset."""
        # Load v1 dataset
        with open(self.v1_dataset_path, 'r') as f:
            v1_data = json.load(f)

        # Extract skeletons
        skeletons = [item['skeleton'] for item in v1_data]

        # Build index
        self.index_builder.build_from_skeletons(skeletons, save=True)

    def generate_prompt(self, v2_skeleton: str, k: int = None,
                        save_prompt: bool = False,
                        target_metrics: dict = None,
                        snippet_id: Any = None) -> Dict[str, Any]:
        """
        Generate few-shot prompt for a v2 skeleton.

        Args:
            v2_skeleton: Target class skeleton from v2
            k: Number of examples to retrieve
            save_prompt: Whether to save prompt to file
            target_metrics: Optional dict of metrics estimated from skeleton
                          (only used if use_metric_filtering=True)
            snippet_id: Optional snippet ID for naming saved files

        Returns:
            Dictionary with prompt and retrieved examples
        """
        logger.info("Generating prompt for v2 skeleton")

        # Step 1: Retrieve similar examples (with optional metric filtering)
        examples = self.rag_retriever.retrieve(v2_skeleton, k=k, target_metrics=target_metrics)

        # Step 2: Build prompt
        messages = self.prompt_builder.build_messages(v2_skeleton, examples)

        # Step 3: Save if requested
        if save_prompt:
            if snippet_id is not None:
                output_path = Path(Config.PROMPTS_DIR) / f"prompt_{snippet_id}.json"
            else:
                output_path = Path(Config.PROMPTS_DIR) / f"prompt_{hash(v2_skeleton)}.json"
            self.prompt_builder.save_messages(messages, str(output_path))

        return {
            'messages': messages,
            'examples': examples,
            'num_examples': len(examples),
            'v2_skeleton': v2_skeleton,
            'used_metric_filtering': self.use_metric_filtering and target_metrics is not None
        }

    def process_v2_dataset(self, v2_dataset_path: str,
                           output_file: str = None, k: int = None):
        """
        Process entire v2 dataset and generate prompts.

        Args:
            v2_dataset_path: Path to v2 dataset
            output_file: Path to save results
            k: Number of examples per query
        """
        logger.info(f"Processing v2 dataset: {v2_dataset_path}")

        # Load v2 dataset
        with open(v2_dataset_path, 'r') as f:
            v2_data = json.load(f)

        results = []

        for i, item in enumerate(v2_data):
            logger.info(f"Processing {i + 1}/{len(v2_data)}: {item.get('class_name', 'Unknown')}")

            v2_skeleton = item['skeleton']
            snippet_id = item.get('snippet_id', i)  # Use snippet_id if available, else index

            # Generate prompt
            result = self.generate_prompt(v2_skeleton, k=k, save_prompt=True, snippet_id=snippet_id)

            # Add metadata
            result['class_name'] = item.get('class_name', 'Unknown')
            result['snippet_id'] = snippet_id
            result['v2_index'] = i

            # Add example info
            result['retrieved_examples'] = [
                {
                    'class_name': ex.class_name,
                    'similarity_score': float(ex.similarity_score),  # Convert to Python float
                    'v1_index': int(ex.index)  # Convert to Python int
                }
                for ex in result['examples']
            ]

            # Remove full example objects (too large)
            del result['examples']

            results.append(result)

        # Save results
        output_file = output_file or Path(Config.RESULTS_DIR) / "v2_prompts_results.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

        logger.info(f"Processed {len(results)} v2 examples")
        logger.info(f"Results saved to {output_file}")

        return results

    def batch_generate_prompts(self, v2_skeletons: List[str], k: int = None) -> List[str]:
        """
        Generate prompts for multiple v2 skeletons.

        Args:
            v2_skeletons: List of v2 skeletons
            k: Number of examples per query

        Returns:
            List of generated prompts
        """
        prompts = []

        for i, skeleton in enumerate(v2_skeletons):
            logger.info(f"Generating prompt {i + 1}/{len(v2_skeletons)}")
            result = self.generate_prompt(skeleton, k=k)
            prompts.append(result['prompt'])

        return prompts

    def get_statistics(self) -> Dict[str, Any]:
        """Get pipeline statistics."""
        return {
            'v1_dataset_size': self.dataset_retriever.get_dataset_size(),
            'index_size': self.index_builder.indexer.get_index_size(),
            'embedding_dimension': self.embedder.get_embedding_dimension(),
            'top_k': Config.TOP_K_EXAMPLES
        }


def main():
    """Example usage of RAG pipeline."""
    import argparse

    parser = argparse.ArgumentParser(description='RAG Pipeline for Class Generation')
    parser.add_argument('--v1-dataset', required=True, help='Path to v1 dataset JSON')
    parser.add_argument('--v2-dataset', help='Path to v2 dataset JSON (for batch processing)')
    parser.add_argument('--v2-skeleton', help='Single v2 skeleton to process')
    parser.add_argument('--rebuild-index', action='store_true', help='Rebuild FAISS index')
    parser.add_argument('--use-metrics', action='store_true', help='Use metrics for filtering (optional)')
    parser.add_argument('-k', type=int, default=3, help='Number of examples to retrieve')
    parser.add_argument('--output', help='Output file path')

    args = parser.parse_args()

    # Initialize pipeline
    pipeline = RAGPipeline(
        v1_dataset_path=args.v1_dataset,
        rebuild_index=args.rebuild_index,
        use_metric_filtering=args.use_metrics  # Optional metric filtering
    )

    # Print statistics
    stats = pipeline.get_statistics()
    print("\n" + "=" * 60)
    print("PIPELINE STATISTICS")
    print("=" * 60)
    for key, value in stats.items():
        print(f"{key}: {value}")
    print("=" * 60 + "\n")

    # Process based on input
    if args.v2_dataset:
        # Batch process v2 dataset
        results = pipeline.process_v2_dataset(
            args.v2_dataset,
            output_file=args.output,
            k=args.k
        )
        print(f"\nProcessed {len(results)} examples from v2 dataset")

    elif args.v2_skeleton:
        # Single skeleton processing
        result = pipeline.generate_prompt(args.v2_skeleton, k=args.k, save_prompt=True)

        print("\n" + "=" * 60)
        print("GENERATED PROMPT")
        print("=" * 60)
        print(result['prompt'])
        print("\n" + "=" * 60)
        print(f"Retrieved {result['num_examples']} examples")

    else:
        print("Please provide either --v2-dataset or --v2-skeleton")


if __name__ == "__main__":
    main()