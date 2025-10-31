"""
Configuration settings for RAG pipeline.
"""

from pathlib import Path


class Config:
    """Configuration for RAG-based class generation."""

    # Model settings
    EMBEDDING_MODEL = "microsoft/graphcodebert-base"  # "microsoft/graphcodebert-base" or "microsoft/codebert-base" or "microsoft/unixcoder-base"
    MAX_SEQUENCE_LENGTH = 512

    # Retrieval settings
    TOP_K_EXAMPLES = 3  # Number of similar examples to retrieve
    SIMILARITY_METRIC = "cosine"  # l2 or cosine

    # Metrics settings (optional)
    USE_METRICS_FOR_FILTERING = False  # Whether to use metrics for filtering
    METRIC_TOLERANCE = {
        'CountDeclMethod': 2,  # +/- 2 methods
        'Cyclomatic': 5,  # +/- 5 complexity points
        'CountLineCode': 50  # +/- 50 lines
    }

    # Data paths
    V1_DATASET_PATH = "../../rag_experiments/csn.json"
    V2_DATASET_PATH = "../../rag_experiments/post_cut-off.json"
    INDEX_SAVE_PATH = "../../rag_experiments/faiss_index"
    EMBEDDINGS_SAVE_PATH = "../../rag_experiments/csn_embeddings.npy"

    # Output paths
    OUTPUT_DIR = "../../rag_experiments/output"
    PROMPTS_DIR = "../../rag_experiments/output/prompts"
    RESULTS_DIR = "../../rag_experiments/output/results"

    # Device settings
    DEVICE = "cpu"  # or "cuda" if you have GPU
    BATCH_SIZE = 32  # For batch embedding generation

    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist."""
        Path(cls.OUTPUT_DIR).mkdir(exist_ok=True)
        Path(cls.PROMPTS_DIR).mkdir(exist_ok=True)
        Path(cls.RESULTS_DIR).mkdir(exist_ok=True)
        Path("../../rag_experiments").mkdir(exist_ok=True)