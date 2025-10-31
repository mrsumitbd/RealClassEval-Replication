import re
from dataclasses import dataclass
from typing import Dict, Iterator, List, Literal, Optional, Union
from chonkie.utils import Hubbie

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
    delimiters: Optional[Union[str, List[str]]] = None
    whitespace: bool = False
    include_delim: Optional[Literal['prev', 'next']] = 'prev'
    pattern: Optional[str] = None
    pattern_mode: Literal['split', 'extract'] = 'split'

    def _validate_fields(self) -> None:
        """Validate all fields have legal values."""
        active_options = sum([bool(self.delimiters), self.whitespace, bool(self.pattern)])
        if active_options > 1:
            raise NotImplementedError('Cannot use multiple splitting methods simultaneously. Choose one of: delimiters, whitespace, or pattern.')
        if self.delimiters is not None:
            if isinstance(self.delimiters, str) and len(self.delimiters) == 0:
                raise ValueError('Custom delimiters cannot be an empty string.')
            if isinstance(self.delimiters, list):
                if any((not isinstance(delim, str) or len(delim) == 0 for delim in self.delimiters)):
                    raise ValueError('Custom delimiters cannot be an empty string.')
                if any((delim == ' ' for delim in self.delimiters)):
                    raise ValueError('Custom delimiters cannot be whitespace only. Set whitespace to True instead.')
        if self.pattern is not None:
            if not isinstance(self.pattern, str) or len(self.pattern) == 0:
                raise ValueError('Pattern must be a non-empty string.')
            try:
                re.compile(self.pattern)
            except re.error as e:
                raise ValueError(f'Invalid regex pattern: {e}')
        if self.pattern_mode not in ['split', 'extract']:
            raise ValueError("pattern_mode must be either 'split' or 'extract'.")

    def __post_init__(self) -> None:
        """Validate attributes."""
        self._validate_fields()

    def __repr__(self) -> str:
        """Return a string representation of the RecursiveLevel."""
        return f'RecursiveLevel(delimiters={self.delimiters}, whitespace={self.whitespace}, include_delim={self.include_delim}, pattern={self.pattern}, pattern_mode={self.pattern_mode})'

    def to_dict(self) -> dict:
        """Return the RecursiveLevel as a dictionary."""
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data: dict) -> 'RecursiveLevel':
        """Create RecursiveLevel object from a dictionary."""
        return cls(**data)

    @classmethod
    def from_recipe(cls, name: str, lang: Optional[str]='en') -> 'RecursiveLevel':
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
        hub = Hubbie()
        recipe = hub.get_recipe(name, lang)
        if recipe is not None:
            return cls.from_dict({'delimiters': recipe['recipe']['delimiters'], 'include_delim': recipe['recipe']['include_delim']})
        else:
            raise ValueError(f'Tried getting recipe `{name}_{lang}.json` but it is not available.')