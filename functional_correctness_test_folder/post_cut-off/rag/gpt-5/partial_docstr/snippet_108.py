from dataclasses import dataclass
from typing import Optional, Union, List, Literal, Dict, Tuple
import re


@dataclass
class RecursiveLevel:
    '''RecursiveLevels express the chunking rules at a specific level for the recursive chunker.
    Attributes:
        whitespace (bool): Whether to use whitespace as a delimiter.
        delimiters (Optional[Union[str, List[str]]]): Custom delimiters for chunking.
        include_delim (Optional[Literal["prev", "next"]]): Whether to include the delimiter at all, or in the previous chunk, or the next chunk.
        pattern (Optional[str]): Regex pattern for advanced splitting/extraction.
        pattern_mode (Literal["split", "extract"]): Whether to split on pattern matches or extract pattern matches.
    '''
    whitespace: bool = False
    delimiters: Optional[Union[str, List[str]]] = None
    include_delim: Optional[Literal["prev", "next"]] = None
    pattern: Optional[str] = None
    pattern_mode: Literal["split", "extract"] = "split"

    def _validate_fields(self) -> None:
        '''Validate all fields have legal values.'''
        methods_selected = sum([
            bool(self.whitespace),
            self.delimiters is not None,
            self.pattern is not None,
        ])
        if methods_selected == 0:
            raise ValueError(
                'One of whitespace, delimiters, or pattern must be specified.')
        if methods_selected > 1:
            raise ValueError(
                'Only one of whitespace, delimiters, or pattern may be specified.')

        # Validate delimiters
        if self.delimiters is not None:
            if isinstance(self.delimiters, str):
                if not self.delimiters:
                    raise ValueError('delimiters string must be non-empty.')
            elif isinstance(self.delimiters, (list, tuple)):
                cleaned: List[str] = []
                for d in self.delimiters:
                    if not isinstance(d, str):
                        raise ValueError('Each delimiter must be a string.')
                    if d:
                        if d not in cleaned:
                            cleaned.append(d)
                if not cleaned:
                    raise ValueError(
                        'delimiters list must contain at least one non-empty string.')
                # Normalize to list
                self.delimiters = cleaned
            else:
                raise ValueError(
                    'delimiters must be a string or a list of strings.')

        # Validate include_delim usage
        if self.include_delim is not None:
            if self.include_delim not in ('prev', 'next'):
                raise ValueError(
                    'include_delim must be either "prev" or "next" if provided.')
            # include_delim only makes sense when splitting on a delimiter/pattern
            if self.whitespace:
                raise ValueError(
                    'include_delim cannot be used with whitespace splitting.')
            if self.pattern is None and self.delimiters is None:
                raise ValueError(
                    'include_delim requires delimiters or a pattern to be specified.')
            if self.pattern is not None and self.pattern_mode != 'split':
                raise ValueError(
                    'include_delim can only be used when pattern_mode is "split".')

        # Validate pattern and pattern_mode
        if self.pattern is not None:
            if not isinstance(self.pattern, str) or not self.pattern:
                raise ValueError(
                    'pattern must be a non-empty string if provided.')
            try:
                re.compile(self.pattern)
            except re.error as e:
                raise ValueError(f'Invalid regex pattern: {e}') from e
            if self.pattern_mode not in ('split', 'extract'):
                raise ValueError('pattern_mode must be "split" or "extract".')
        else:
            # No pattern: only allow default split; extract makes no sense without a pattern
            if self.pattern_mode != 'split':
                raise ValueError('pattern_mode "extract" requires a pattern.')

    def __post_init__(self) -> None:
        '''Validate attributes.'''
        self._validate_fields()

    def __repr__(self) -> str:
        '''Return a string representation of the RecursiveLevel.'''
        parts = []
        if self.whitespace:
            parts.append('whitespace=True')
        if self.delimiters is not None:
            parts.append(f'delimiters={self.delimiters!r}')
        if self.include_delim is not None:
            parts.append(f'include_delim={self.include_delim!r}')
        if self.pattern is not None:
            parts.append(f'pattern={self.pattern!r}')
            parts.append(f'pattern_mode={self.pattern_mode!r}')
        return f"RecursiveLevel({', '.join(parts)})"

    def to_dict(self) -> dict:
        '''Return the RecursiveLevel as a dictionary.'''
        data: Dict[str, object] = {}
        if self.whitespace:
            data['whitespace'] = True
        if self.delimiters is not None:
            data['delimiters'] = self.delimiters
        if self.include_delim is not None:
            data['include_delim'] = self.include_delim
        if self.pattern is not None:
            data['pattern'] = self.pattern
            data['pattern_mode'] = self.pattern_mode
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'RecursiveLevel':
        '''Create RecursiveLevel object from a dictionary.'''
        if not isinstance(data, dict):
            raise ValueError('data must be a dictionary.')
        kwargs: Dict[str, object] = {}
        if 'whitespace' in data:
            kwargs['whitespace'] = bool(data['whitespace'])
        if 'delimiters' in data:
            delims = data['delimiters']
            if isinstance(delims, (list, tuple)):
                kwargs['delimiters'] = list(delims)
            else:
                kwargs['delimiters'] = delims
        if 'include_delim' in data:
            kwargs['include_delim'] = data['include_delim']
        if 'pattern' in data:
            kwargs['pattern'] = data['pattern']
        if 'pattern_mode' in data:
            kwargs['pattern_mode'] = data['pattern_mode']
        return cls(**kwargs)

    @classmethod
    def from_recipe(cls, name: str, lang: Optional[str] = 'en') -> 'RecursiveLevel':
        '''Create RecursiveLevel object from a recipe.
        The recipes are registered in the [Chonkie Recipe Store](https://huggingface.co/datasets/chonkie-ai/recipes). If the recipe is not there, you can create your own recipe and share it with the community!
        Args:
            name (str): The name of the recipe.
            lang (Optional[str]): The language of the recipe.
        Returns:
            RecursiveLevel: The RecursiveLevel object.
        Raises:
            ValueError: If the recipe is not found.
        '''
        # Minimal built-in recipe registry
        recipes: Dict[Tuple[str, str], Dict[str, object]] = {
            ('whitespace', 'en'): {'whitespace': True},
            ('newline', 'en'): {'delimiters': ['\n\n', '\n'], 'include_delim': 'next'},
            ('paragraph', 'en'): {'delimiters': ['\n\n']},
            ('sentence', 'en'): {'pattern': r'(?<=[.!?])\s+', 'pattern_mode': 'split'},
            ('markdown_headings', 'en'): {'pattern': r'(?=^#+\s)', 'pattern_mode': 'extract'},
            ('code_block', 'en'): {'pattern': r'```[\s\S]*?```', 'pattern_mode': 'extract'},
        }
        key = (name, lang or 'en')
        if key not in recipes:
            raise ValueError(f'Recipe not found: name="{name}", lang="{lang}"')
        return cls.from_dict(recipes[key])
