
from dataclasses import dataclass, field
from typing import Optional, Union, List, Literal
import requests


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

    whitespace: bool
    delimiters: Optional[Union[str, List[str]]] = None
    include_delim: Optional[Literal["prev", "next"]] = None
    pattern: Optional[str] = None
    pattern_mode: Literal["split", "extract"] = "split"

    def _validate_fields(self) -> None:
        '''Validate all fields have legal values.'''
        if self.include_delim not in [None, "prev", "next"]:
            raise ValueError(
                "include_delim must be one of None, 'prev', or 'next'")
        if self.pattern_mode not in ["split", "extract"]:
            raise ValueError(
                "pattern_mode must be one of 'split' or 'extract'")

    def __post_init__(self) -> None:
        '''Validate attributes.'''
        self._validate_fields()

    def __repr__(self) -> str:
        '''Return a string representation of the RecursiveLevel.'''
        return (f"RecursiveLevel(whitespace={self.whitespace}, "
                f"delimiters={self.delimiters}, include_delim={self.include_delim}, "
                f"pattern={self.pattern}, pattern_mode={self.pattern_mode})")

    def to_dict(self) -> dict:
        '''Return the RecursiveLevel as a dictionary.'''
        return {
            "whitespace": self.whitespace,
            "delimiters": self.delimiters,
            "include_delim": self.include_delim,
            "pattern": self.pattern,
            "pattern_mode": self.pattern_mode
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'RecursiveLevel':
        '''Create RecursiveLevel object from a dictionary.'''
        return cls(**data)

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
        url = f"https://huggingface.co/datasets/chonkie-ai/recipes/resolve/main/{lang}/{name}.json"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(
                f"Recipe '{name}' not found for language '{lang}'.")
        data = response.json()
        return cls.from_dict(data)
