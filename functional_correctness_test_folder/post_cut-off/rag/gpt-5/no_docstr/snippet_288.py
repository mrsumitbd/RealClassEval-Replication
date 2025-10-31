from __future__ import annotations

from dataclasses import dataclass, is_dataclass, asdict
from typing import Any, Dict
import base64


@dataclass
class ParserExtensionConfig:
    '''Parser extension configuration.'''
    @staticmethod
    def encode_base64(text: str) -> str:
        '''Encode a string to base64.
        Args:
            log: Raw string
        Returns:
            Base64 encoded string
        '''
        if not isinstance(text, str):
            raise TypeError('encode_base64 expects a string')
        return base64.b64encode(text.encode('utf-8')).decode('ascii')

    def __post_init__(self) -> None:
        '''Post initialization hook for field processing.'''
        # No fields defined; hook reserved for future processing.
        return

    def validate(self) -> None:
        '''Validate configuration.
        Raises:
            ValueError: If configuration is invalid
        '''
        # No intrinsic rules by default; override or extend as needed.
        return

    def to_dict(self) -> Dict:
        '''Convert to dictionary format for API request.
        Returns:
            Dict containing the configuration in API format
        Raises:
            ValueError: If configuration is invalid
        '''
        self.validate()

        def convert(value: Any) -> Any:
            if value is None or isinstance(value, (str, int, float, bool)):
                return value
            if isinstance(value, bytes):
                return base64.b64encode(value).decode('ascii')
            if isinstance(value, (list, tuple, set)):
                return [convert(v) for v in value]
            if isinstance(value, dict):
                return {str(k): convert(v) for k, v in value.items() if not callable(v)}
            if hasattr(value, 'to_dict') and callable(getattr(value, 'to_dict')):
                return value.to_dict()
            if is_dataclass(value):
                return {k: convert(v) for k, v in asdict(value).items()}
            return str(value)

        # Include all public attributes set on the instance
        data = {k: v for k, v in self.__dict__.items(
        ) if not k.startswith('_') and not callable(v)}
        return convert(data)
