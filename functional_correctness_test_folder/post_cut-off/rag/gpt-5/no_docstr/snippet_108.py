from dataclasses import dataclass
from typing import Optional, Union, List, Literal, Dict, Any
import json
import re


@dataclass
class RecursiveLevel:
    """RecursiveLevels express the chunking rules at a specific level for the recursive chunker.
    Attributes:
        whitespace (bool): Whether to use whitespace as a delimiter.
        delimiters (Optional[Union[str, List[str]]]): Custom delimiters for chunking.
        include_delim (Optional[Literal["prev", "next"]]): Whether to include the delimiter at all, or in the previous chunk, or the next chunk.
        pattern (Optional[str]): Regex pattern for advanced splitting/extraction.
        pattern_mode (Literal["split", "extract"]): Whether to split on pattern matches or extract pattern matches.
    """

    whitespace: bool = False
    delimiters: Optional[Union[str, List[str]]] = None
    include_delim: Optional[Literal["prev", "next"]] = None
    pattern: Optional[str] = None
    pattern_mode: Literal["split", "extract"] = "split"

    def _validate_fields(self) -> None:
        """Validate all fields have legal values."""
        if not isinstance(self.whitespace, bool):
            raise TypeError('whitespace must be a bool.')

        if self.delimiters is not None:
            if isinstance(self.delimiters, str):
                if self.delimiters == '':
                    raise ValueError('delimiters string must be non-empty.')
            elif isinstance(self.delimiters, list):
                if len(self.delimiters) == 0:
                    raise ValueError('delimiters list must be non-empty.')
                for i, d in enumerate(self.delimiters):
                    if not isinstance(d, str) or d == '':
                        raise ValueError(
                            f'delimiters[{i}] must be a non-empty string.')
            else:
                raise TypeError(
                    'delimiters must be a string, list of strings, or None.')

        if self.include_delim is not None and self.include_delim not in ('prev', 'next'):
            raise ValueError(
                "include_delim must be one of 'prev', 'next', or None.")

        if self.pattern is not None:
            if not isinstance(self.pattern, str) or self.pattern == '':
                raise ValueError(
                    'pattern must be a non-empty string when provided.')
            try:
                re.compile(self.pattern)
            except re.error as e:
                raise ValueError(
                    f'pattern is not a valid regular expression: {e}') from e

        if self.pattern_mode not in ('split', 'extract'):
            raise ValueError("pattern_mode must be 'split' or 'extract'.")

        if not self.whitespace and self.delimiters is None and self.pattern is None:
            raise ValueError(
                'At least one of whitespace, delimiters, or pattern must be specified.')

    def __post_init__(self) -> None:
        """Validate attributes."""
        # Normalize delimiters list entries by ensuring they are strings (if list)
        if isinstance(self.delimiters, list):
            self.delimiters = [str(d) for d in self.delimiters]
        self._validate_fields()

    def __repr__(self) -> str:
        """Return a string representation of the RecursiveLevel."""
        return (
            f"RecursiveLevel(whitespace={self.whitespace}, "
            f"delimiters={self.delimiters!r}, "
            f"include_delim={self.include_delim!r}, "
            f"pattern={self.pattern!r}, "
            f"pattern_mode={self.pattern_mode!r})"
        )

    def to_dict(self) -> dict:
        """Return the RecursiveLevel as a dictionary."""
        data: Dict[str, Any] = {
            'whitespace': self.whitespace,
            'pattern_mode': self.pattern_mode,
        }
        if self.delimiters is not None:
            data['delimiters'] = self.delimiters
        if self.include_delim is not None:
            data['include_delim'] = self.include_delim
        if self.pattern is not None:
            data['pattern'] = self.pattern
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'RecursiveLevel':
        """Create RecursiveLevel object from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError('data must be a dict.')
        args: Dict[str, Any] = {}
        if 'whitespace' in data:
            args['whitespace'] = data['whitespace']
        if 'delimiters' in data:
            args['delimiters'] = data['delimiters']
        if 'include_delim' in data:
            args['include_delim'] = data['include_delim']
        if 'pattern' in data:
            args['pattern'] = data['pattern']
        if 'pattern_mode' in data:
            args['pattern_mode'] = data['pattern_mode']
        return cls(**args)

    @classmethod
    def from_recipe(cls, name: str, lang: Optional[str] = 'en') -> 'RecursiveLevel':
        """Create RecursiveLevel object from a recipe.
        The recipes are registered in the [Chonkie Recipe Store](https://huggingface.co/datasets/chonkie-ai/recipes). If the recipe is not there, you can create your own recipe and share it with the community!
        Args:
            name (str): The name of the recipe.
            lang (Optional[str]): The language of the recipe.
        Returns:
            RecursiveLevel: The RecursiveLevel object.
        Raises:
            ValueError: If the recipe is not found.
        """
        if not isinstance(name, str) or name.strip() == '':
            raise ValueError('name must be a non-empty string.')
        if lang is not None and (not isinstance(lang, str) or lang.strip() == ''):
            raise ValueError('lang must be a non-empty string when provided.')
        lang_segment = lang or 'en'

        # Attempt to fetch recipe JSON from Hugging Face dataset repository.
        # Expected layout: datasets/chonkie-ai/recipes/resolve/main/{lang}/{name}.json
        url_candidates = [
            f'https://huggingface.co/datasets/chonkie-ai/recipes/resolve/main/{lang_segment}/{name}.json',
            f'https://huggingface.co/datasets/chonkie-ai/recipes/resolve/main/{name}.json',
        ]

        last_err: Optional[Exception] = None
        payload: Optional[dict] = None

        for url in url_candidates:
            try:
                try:
                    import requests  # type: ignore
                    resp = requests.get(url, timeout=10)
                    if resp.status_code == 200:
                        payload = resp.json()
                        break
                    else:
                        last_err = ValueError(
                            f'HTTP {resp.status_code} for {url}')
                except Exception as e:
                    # Fallback to urllib if requests is unavailable or fails
                    import urllib.request
                    with urllib.request.urlopen(url, timeout=10) as response:
                        if response.status == 200:
                            content = response.read().decode('utf-8')
                            payload = json.loads(content)
                            break
                        else:
                            last_err = ValueError(
                                f'HTTP {response.status} for {url}')
            except Exception as e:
                last_err = e
                continue

        if payload is None:
            raise ValueError(
                f'Could not retrieve recipe "{name}" (lang="{lang_segment}"): {last_err}')

        # If the payload is a dict representing a level, use it directly.
        # If it contains a top-level key like "level" or "levels", attempt to select appropriately.
        if isinstance(payload, dict):
            # If payload appears to be a container with levels, try to extract one.
            if 'level' in payload and isinstance(payload['level'], dict):
                data = payload['level']
            elif 'levels' in payload and isinstance(payload['levels'], list) and payload['levels']:
                # Use first level if multiple are provided.
                data = payload['levels'][0]
            else:
                data = payload
        else:
            raise ValueError(
                f'Unexpected recipe format for "{name}". Expected a JSON object.')

        if not isinstance(data, dict):
            raise ValueError(f'Invalid recipe structure for "{name}".')

        return cls.from_dict(data)
