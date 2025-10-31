from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import base64
import binascii


@dataclass
class ParserExtensionConfig:
    """Parser extension configuration."""
    name: Optional[str] = None
    version: Optional[str] = None
    entrypoint: Optional[str] = None
    code: Optional[str] = None
    code_base64: Optional[str] = None
    enabled: bool = True
    env: Optional[Dict[str, str]] = None
    variables: Optional[Dict[str, Any]] = None
    timeout_ms: Optional[int] = None

    @staticmethod
    def encode_base64(text: str) -> str:
        """Encode a string to base64.
        Args:
            log: Raw string
        Returns:
            Base64 encoded string
        """
        if text is None:
            return ''
        if not isinstance(text, str):
            raise TypeError('text must be a str')
        return base64.b64encode(text.encode('utf-8')).decode('ascii')

    def __post_init__(self) -> None:
        """Post initialization hook for field processing."""
        # Normalize string fields
        for attr in ('name', 'version', 'entrypoint', 'code_base64'):
            val = getattr(self, attr)
            if isinstance(val, str):
                setattr(self, attr, val.strip())

        # Normalize env: ensure dict[str, str]
        if self.env is not None:
            normalized_env: Dict[str, str] = {}
            for k, v in self.env.items():
                key = str(k).strip()
                val = '' if v is None else str(v)
                normalized_env[key] = val
            self.env = normalized_env

        # Ensure variables is a dict if provided
        if self.variables is not None and not isinstance(self.variables, dict):
            # attempt to coerce mapping-like
            self.variables = dict(self.variables)

        # If raw code provided, compute base64 (overrides provided base64)
        if isinstance(self.code, str) and self.code != '':
            self.code_base64 = self.encode_base64(self.code)

        # If base64 provided, strip whitespace/newlines
        if isinstance(self.code_base64, str):
            self.code_base64 = ''.join(self.code_base64.split())

    def validate(self) -> None:
        """Validate configuration.
        Raises:
            ValueError: If configuration is invalid
        """
        # enabled implies code must be present in some form
        if self.enabled and not (isinstance(self.code_base64, str) and self.code_base64):
            raise ValueError(
                'code or code_base64 must be provided when enabled is True')

        if self.name is not None and (not isinstance(self.name, str) or self.name.strip() == ''):
            raise ValueError('name must be a non-empty string when provided')

        if self.version is not None and (not isinstance(self.version, str) or self.version.strip() == ''):
            raise ValueError(
                'version must be a non-empty string when provided')

        if self.entrypoint is not None and (not isinstance(self.entrypoint, str) or self.entrypoint.strip() == ''):
            raise ValueError(
                'entrypoint must be a non-empty string when provided')

        if self.timeout_ms is not None:
            if not isinstance(self.timeout_ms, int) or self.timeout_ms <= 0:
                raise ValueError(
                    'timeout_ms must be a positive integer when provided')

        if self.env is not None:
            if not isinstance(self.env, dict):
                raise ValueError('env must be a dict[str, str] when provided')
            for k, v in self.env.items():
                if not isinstance(k, str) or k.strip() == '':
                    raise ValueError('env keys must be non-empty strings')
                if not isinstance(v, str):
                    raise ValueError('env values must be strings')

        if self.variables is not None:
            if not isinstance(self.variables, dict):
                raise ValueError('variables must be a dict when provided')
            for k in self.variables.keys():
                if not isinstance(k, str) or k.strip() == '':
                    raise ValueError(
                        'variables keys must be non-empty strings')

        # Validate base64 content if present
        if self.code_base64:
            try:
                base64.b64decode(self.code_base64, validate=True)
            except (binascii.Error, ValueError) as e:
                raise ValueError('code_base64 is not valid base64') from e

    def to_dict(self) -> Dict:
        """Convert to dictionary format for API request.
        Returns:
            Dict containing the configuration in API format
        Raises:
            ValueError: If configuration is invalid
        """
        # Ensure base64 is computed if only raw code is present
        if (not self.code_base64) and self.code:
            self.code_base64 = self.encode_base64(self.code)

        self.validate()

        payload: Dict[str, Any] = {
            'name': self.name,
            'version': self.version,
            'entry_point': self.entrypoint,
            'code_base64': self.code_base64,
            'enabled': self.enabled,
            'env': self.env,
            'variables': self.variables,
            'timeout_ms': self.timeout_ms,
        }
        # Remove None values
        return {k: v for k, v in payload.items() if v is not None}
