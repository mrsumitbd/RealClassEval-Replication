from dataclasses import dataclass
from typing import List, Optional, Union, Literal
import re
import json

try:
    import requests  # type: ignore
except Exception:  # pragma: no cover
    requests = None  # type: ignore


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

        # Normalize delimiters
        if self.delimiters is not None:
            if isinstance(self.delimiters, str):
                self.delimiters = [self.delimiters]
            elif isinstance(self.delimiters, list):
                if not all(isinstance(d, str) for d in self.delimiters):
                    raise TypeError('All delimiters must be strings.')
            else:
                raise TypeError(
                    'delimiters must be a string or a list of strings.')
            # Remove empty delimiters and duplicates while preserving order
            seen = set()
            normalized: List[str] = []
            for d in self.delimiters:
                if d is None:
                    continue
                if not isinstance(d, str):
                    raise TypeError('All delimiters must be strings.')
                if d == '':
                    continue
                if d not in seen:
                    seen.add(d)
                    normalized.append(d)
            self.delimiters = normalized if normalized else None

        if self.include_delim is not None:
            if self.include_delim not in ('prev', 'next'):
                raise ValueError(
                    'include_delim must be None, "prev", or "next".')

        if self.pattern is not None:
            if not isinstance(self.pattern, str) or self.pattern.strip() == '':
                raise ValueError(
                    'pattern, if provided, must be a non-empty string.')
            try:
                re.compile(self.pattern)
            except re.error as e:
                raise ValueError(f'Invalid regex pattern: {e}') from e

        if self.pattern_mode not in ('split', 'extract'):
            raise ValueError('pattern_mode must be "split" or "extract".')

        if self.pattern_mode == 'extract' and self.pattern is None:
            raise ValueError(
                'pattern_mode "extract" requires a regex pattern.')

        # At least one strategy should be provided
        if not self.whitespace and self.delimiters is None and self.pattern is None:
            raise ValueError(
                'At least one of whitespace, delimiters, or pattern must be provided.')

        # include_delim should only be meaningful with a delimiter-based split or pattern split
        if self.include_delim is not None and self.pattern_mode == 'extract' and self.delimiters is None and self.pattern is not None:
            # In extract mode, include_delim has no effect; allow but warn silently by clearing
            self.include_delim = None

    def __post_init__(self) -> None:
        """Validate attributes."""
        # Normalize include_delim to lowercase if provided
        if isinstance(self.include_delim, str):
            # type: ignore[assignment]
            self.include_delim = self.include_delim.lower()
        # Normalize pattern_mode
        if isinstance(self.pattern_mode, str):
            # type: ignore[assignment]
            self.pattern_mode = self.pattern_mode.lower()
        self._validate_fields()

    def __repr__(self) -> str:
        """Return a string representation of the RecursiveLevel."""
        return (
            f"RecursiveLevel(whitespace={self.whitespace}, "
            f"delimiters={self.delimiters}, "
            f"include_delim={self.include_delim}, "
            f"pattern={repr(self.pattern)}, "
            f"pattern_mode='{self.pattern_mode}')"
        )

    def to_dict(self) -> dict:
        """Return the RecursiveLevel as a dictionary."""
        return {
            'whitespace': self.whitespace,
            'delimiters': self.delimiters,
            'include_delim': self.include_delim,
            'pattern': self.pattern,
            'pattern_mode': self.pattern_mode,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'RecursiveLevel':
        """Create RecursiveLevel object from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError('data must be a dict.')
        kwargs = {
            'whitespace': data.get('whitespace', False),
            'delimiters': data.get('delimiters'),
            'include_delim': data.get('include_delim'),
            'pattern': data.get('pattern'),
            'pattern_mode': data.get('pattern_mode', 'split'),
        }
        return cls(**kwargs)

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
        # Built-in minimal registry for common recipes as a fallback
        builtin_registry = {
            ('en', 'basic'): {
                'whitespace': True,
                'delimiters': ['\n\n', '\n', ' '],
                'include_delim': None,
                'pattern': None,
                'pattern_mode': 'split',
            },
            ('en', 'sentences'): {
                'whitespace': False,
                'delimiters': None,
                'include_delim': None,
                'pattern': r'(?<=[.!?])\s+',
                'pattern_mode': 'split',
            },
            ('en', 'code_blocks'): {
                'whitespace': False,
                'delimiters': ['\n```', '```', '\n\n'],
                'include_delim': 'prev',
                'pattern': None,
                'pattern_mode': 'split',
            },
        }

        # Try fetching from Hugging Face if possible
        urls_to_try: List[str] = []
        safe_lang = (lang or 'en').strip('/')
        safe_name = name.strip('/')

        # Attempt common locations
        urls_to_try.append(
            f'https://huggingface.co/datasets/chonkie-ai/recipes/resolve/main/{safe_lang}/{safe_name}.json'
        )
        urls_to_try.append(
            f'https://huggingface.co/datasets/chonkie-ai/recipes/resolve/main/{safe_name}.json'
        )
        urls_to_try.append(
            f'https://huggingface.co/datasets/chonkie-ai/recipes/resolve/main/{safe_lang}/{safe_name}.yaml'
        )
        urls_to_try.append(
            f'https://huggingface.co/datasets/chonkie-ai/recipes/resolve/main/{safe_name}.yaml'
        )

        recipe_data: Optional[dict] = None

        if requests is not None:
            for url in urls_to_try:
                try:
                    resp = requests.get(url, timeout=5)
                    if resp.status_code == 200:
                        text = resp.text.strip()
                        if not text:
                            continue
                        # Try JSON first
                        try:
                            data = json.loads(text)
                        except Exception:
                            # Try very simple YAML-like parsing for key: value pairs
                            data = {}
                            for line in text.splitlines():
                                line = line.strip()
                                if not line or line.startswith('#') or ':' not in line:
                                    continue
                                k, v = line.split(':', 1)
                                k = k.strip()
                                v = v.strip().strip('"').strip("'")
                                # rudimentary parsing for lists
                                if v.startswith('[') and v.endswith(']'):
                                    inner = v[1:-1].strip()
                                    if inner:
                                        parts = [p.strip().strip('"').strip("'")
                                                 for p in inner.split(',')]
                                        data[k] = parts
                                    else:
                                        data[k] = []
                                elif v.lower() in ('true', 'false'):
                                    data[k] = v.lower() == 'true'
                                elif v.lower() in ('null', 'none'):
                                    data[k] = None
                                else:
                                    data[k] = v
                        # If recipe seems to have multiple levels
                        if isinstance(data, dict):
                            if any(k in data for k in ('whitespace', 'delimiters', 'pattern', 'pattern_mode', 'include_delim')):
                                recipe_data = data
                                break
                            if 'level' in data and isinstance(data['level'], dict):
                                recipe_data = data['level']
                                break
                            if 'levels' in data and isinstance(data['levels'], list) and data['levels']:
                                # Choose the first level by default
                                first = data['levels'][0]
                                if isinstance(first, dict):
                                    recipe_data = first
                                    break
                except Exception:
                    continue

        if recipe_data is None:
            recipe_data = builtin_registry.get((safe_lang, safe_name))

        if recipe_data is None:
            raise ValueError(f'Recipe "{name}" (lang="{lang}") not found.')

        return cls.from_dict(recipe_data)
