from typing import Dict, Optional, Any, Union
import argparse
import os

class SearchAssistantConfig:
    """Configuration class for the Search Assistant."""

    def __init__(self, args: argparse.Namespace):
        """Initialize configuration from command line arguments.

        Args:
            args: Parsed command line arguments.
        """
        self.model_path: str = args.model_name_or_path
        self.temperature: float = args.temperature
        self.top_p: float = args.top_p
        self.max_tokens: int = args.max_tokens
        self.max_turns: int = args.max_turns
        self.interactive: bool = args.interactive
        self.generate_summary: bool = not args.no_summary
        self.query: Optional[str] = getattr(args, 'query', None)
        self.tensor_parallel_size: int = 1
        self.rope_scaling: Dict[str, Union[str, float, int]] = {'rope_type': 'yarn', 'factor': 4.0, 'original_max_position_embeddings': 32768}
        self.max_model_len: int = 128000
        self.trust_remote_code: bool = True

    def validate(self) -> None:
        """Validate configuration parameters.

        Raises:
            ValueError: If any configuration parameter is invalid.
        """
        if self.temperature < 0.0 or self.temperature > 2.0:
            raise ValueError('Temperature must be between 0.0 and 2.0')
        if self.top_p < 0.0 or self.top_p > 1.0:
            raise ValueError('Top-p must be between 0.0 and 1.0')
        if self.max_tokens <= 0:
            raise ValueError('Max tokens must be positive')
        if self.max_turns <= 0:
            raise ValueError('Max turns must be positive')
        if not os.path.exists(self.model_path) and (not self.model_path.startswith(('hf://', 'https://'))):
            logger.warning(f'Model path may not exist: {self.model_path}')