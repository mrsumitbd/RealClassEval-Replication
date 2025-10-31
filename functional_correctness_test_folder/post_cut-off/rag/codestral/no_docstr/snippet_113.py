
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
    llm: str = 'gpt-3.5-turbo'
    timeout_seconds: int = 300
    path: str = './data'
    max_retries: int = 3
    temperature: float = 0.7
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    api_key: str | None = None

    def __post_init__(self):
        '''Load any environment variable overrides if they exist.'''
        import os
        env_vars = {
            'BIONMI_LLM': 'llm',
            'BIONMI_TIMEOUT': 'timeout_seconds',
            'BIONMI_PATH': 'path',
            'BIONMI_MAX_RETRIES': 'max_retries',
            'BIONMI_TEMPERATURE': 'temperature',
            'BIONMI_TOP_P': 'top_p',
            'BIONMI_FREQUENCY_PENALTY': 'frequency_penalty',
            'BIONMI_PRESENCE_PENALTY': 'presence_penalty',
            'BIONMI_API_KEY': 'api_key'
        }

        for env_var, attr in env_vars.items():
            if env_var in os.environ:
                value = os.environ[env_var]
                if attr in ['timeout_seconds', 'max_retries']:
                    setattr(self, attr, int(value))
                elif attr in ['temperature', 'top_p', 'frequency_penalty', 'presence_penalty']:
                    setattr(self, attr, float(value))
                else:
                    setattr(self, attr, value)

    def to_dict(self) -> dict:
        '''Convert config to dictionary for easy access.'''
        return {
            'llm': self.llm,
            'timeout_seconds': self.timeout_seconds,
            'path': self.path,
            'max_retries': self.max_retries,
            'temperature': self.temperature,
            'top_p': self.top_p,
            'frequency_penalty': self.frequency_penalty,
            'presence_penalty': self.presence_penalty,
            'api_key': self.api_key
        }
