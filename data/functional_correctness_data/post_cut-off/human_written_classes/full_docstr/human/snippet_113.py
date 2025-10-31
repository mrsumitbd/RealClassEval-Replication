import os
from dataclasses import dataclass

@dataclass
class BiomniConfig:
    """Central configuration for Biomni agent.

    All settings are optional and have sensible defaults.
    API keys are still read from environment variables to maintain
    compatibility with existing .env file structure.

    Usage:
        # Create config with defaults
        config = BiomniConfig()

        # Override specific settings
        config = BiomniConfig(llm="gpt-4", timeout_seconds=1200)

        # Modify after creation
        config.path = "./custom_data"
    """
    path: str = './data'
    timeout_seconds: int = 600
    llm: str = 'claude-sonnet-4-20250514'
    temperature: float = 0.7
    use_tool_retriever: bool = True
    base_url: str | None = None
    api_key: str | None = None
    source: str | None = None

    def __post_init__(self):
        """Load any environment variable overrides if they exist."""
        if os.getenv('BIOMNI_PATH') or os.getenv('BIOMNI_DATA_PATH'):
            self.path = os.getenv('BIOMNI_PATH') or os.getenv('BIOMNI_DATA_PATH')
        if os.getenv('BIOMNI_TIMEOUT_SECONDS'):
            self.timeout_seconds = int(os.getenv('BIOMNI_TIMEOUT_SECONDS'))
        if os.getenv('BIOMNI_LLM') or os.getenv('BIOMNI_LLM_MODEL'):
            self.llm = os.getenv('BIOMNI_LLM') or os.getenv('BIOMNI_LLM_MODEL')
        if os.getenv('BIOMNI_USE_TOOL_RETRIEVER'):
            self.use_tool_retriever = os.getenv('BIOMNI_USE_TOOL_RETRIEVER').lower() == 'true'
        if os.getenv('BIOMNI_TEMPERATURE'):
            self.temperature = float(os.getenv('BIOMNI_TEMPERATURE'))
        if os.getenv('BIOMNI_CUSTOM_BASE_URL'):
            self.base_url = os.getenv('BIOMNI_CUSTOM_BASE_URL')
        if os.getenv('BIOMNI_CUSTOM_API_KEY'):
            self.api_key = os.getenv('BIOMNI_CUSTOM_API_KEY')
        if os.getenv('BIOMNI_SOURCE'):
            self.source = os.getenv('BIOMNI_SOURCE')

    def to_dict(self) -> dict:
        """Convert config to dictionary for easy access."""
        return {'path': self.path, 'timeout_seconds': self.timeout_seconds, 'llm': self.llm, 'temperature': self.temperature, 'use_tool_retriever': self.use_tool_retriever, 'base_url': self.base_url, 'api_key': self.api_key, 'source': self.source}