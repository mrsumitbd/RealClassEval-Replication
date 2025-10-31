from pathlib import Path

class MedicalSearchConfig:
    """Configuration class for the Medical Search Server."""

    def __init__(self):
        self.local_storage = LOCAL_STORAGE
        self.rag_url = RAG_URL
        self.model_name = 'meoconxinhxan/MedicalBm25-PubMed'
        self.timeout = 6000
        self.max_results = 50
        self.preview_length = 256

    def validate(self) -> None:
        """Validate configuration parameters."""
        if not self.local_storage:
            raise ValueError('LOCAL_STORAGE must be specified')
        if not self.rag_url:
            raise ValueError('RAG_URL must be specified')
        Path(self.local_storage).mkdir(parents=True, exist_ok=True)
        logger.info(f'Using storage directory: {self.local_storage}')