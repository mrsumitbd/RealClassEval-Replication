from typing import Dict, Any, Optional, Union
import base64
import json
from dataclasses import dataclass, field

@dataclass
class ParserExtensionConfig:
    """Parser extension configuration."""
    log: Optional[str] = None
    parser_config: Optional[str] = None
    field_extractors: Optional[Union[Dict, str]] = None
    dynamic_parsing: Optional[Union[Dict, str]] = None
    encoded_log: Optional[str] = field(init=False, default=None)
    encoded_cbn_snippet: Optional[str] = field(init=False, default=None)

    @staticmethod
    def encode_base64(text: str) -> str:
        """Encode a string to base64.

        Args:
            log: Raw string

        Returns:
            Base64 encoded string
        """
        if not text:
            raise ValueError('Value cannot be empty for encoding')
        try:
            decoded = base64.b64decode(text)
            decoded.decode('utf-8')
            return text
        except Exception:
            return base64.b64encode(text.encode('utf-8')).decode('utf-8')

    def __post_init__(self) -> None:
        """Post initialization hook for field processing."""
        if self.log:
            self.encoded_log = self.encode_base64(self.log)
        if self.parser_config:
            self.encoded_cbn_snippet = self.encode_base64(self.parser_config)
        if self.field_extractors and isinstance(self.field_extractors, str):
            try:
                self.field_extractors = json.loads(self.field_extractors)
            except json.JSONDecodeError as e:
                raise ValueError(f'Invalid JSON for field_extractors: {e}') from e
        if self.dynamic_parsing and isinstance(self.dynamic_parsing, str):
            try:
                self.dynamic_parsing = json.loads(self.dynamic_parsing)
            except json.JSONDecodeError as e:
                raise ValueError(f'Invalid JSON for dynamic_parsing: {e}') from e

    def validate(self) -> None:
        """Validate configuration.

        Raises:
            ValueError: If configuration is invalid
        """
        config_count = sum((1 for x in [self.parser_config, self.field_extractors, self.dynamic_parsing] if x is not None))
        if config_count != 1:
            raise ValueError('Exactly one of parser_config, field_extractors, or dynamic_parsing must be specified')

    def to_dict(self) -> Dict:
        """Convert to dictionary format for API request.

        Returns:
            Dict containing the configuration in API format

        Raises:
            ValueError: If configuration is invalid
        """
        self.validate()
        config = {}
        if self.encoded_log is not None:
            config['log'] = self.encoded_log
        if self.parser_config is not None:
            config['cbn_snippet'] = self.encoded_cbn_snippet
        elif self.field_extractors is not None:
            config['field_extractors'] = self.field_extractors
        elif self.dynamic_parsing is not None:
            config['dynamic_parsing'] = self.dynamic_parsing
        return config