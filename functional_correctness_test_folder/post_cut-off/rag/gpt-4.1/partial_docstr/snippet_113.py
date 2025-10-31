from dataclasses import dataclass, field, asdict
import os


@dataclass
class BiomniConfig:
    '''Central configuration for Biomni agent.
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
    '''
    llm: str = "gpt-3.5-turbo"
    timeout_seconds: int = 600
    path: str = "./data"
    log_level: str = "INFO"
    max_tokens: int = 2048
    temperature: float = 0.7
    api_base_url: str = "https://api.openai.com/v1"
    # Add more config fields as needed

    def __post_init__(self):
        '''Load any environment variable overrides if they exist.'''
        # Example: allow override from environment variables
        if "BIOMNI_LLM" in os.environ:
            self.llm = os.environ["BIOMNI_LLM"]
        if "BIOMNI_TIMEOUT_SECONDS" in os.environ:
            try:
                self.timeout_seconds = int(
                    os.environ["BIOMNI_TIMEOUT_SECONDS"])
            except ValueError:
                pass
        if "BIOMNI_PATH" in os.environ:
            self.path = os.environ["BIOMNI_PATH"]
        if "BIOMNI_LOG_LEVEL" in os.environ:
            self.log_level = os.environ["BIOMNI_LOG_LEVEL"]
        if "BIOMNI_MAX_TOKENS" in os.environ:
            try:
                self.max_tokens = int(os.environ["BIOMNI_MAX_TOKENS"])
            except ValueError:
                pass
        if "BIOMNI_TEMPERATURE" in os.environ:
            try:
                self.temperature = float(os.environ["BIOMNI_TEMPERATURE"])
            except ValueError:
                pass
        if "BIOMNI_API_BASE_URL" in os.environ:
            self.api_base_url = os.environ["BIOMNI_API_BASE_URL"]

    def to_dict(self) -> dict:
        '''Convert config to dictionary for easy access.'''
        return asdict(self)
