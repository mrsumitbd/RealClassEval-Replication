
from dataclasses import dataclass
from typing import Optional, Union, List, Literal
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
        if self.pattern is not None and not isinstance(self.pattern, str):
            raise ValueError("Pattern must be a string or None.")
        if self.pattern_mode not in ["split", "extract"]:
            raise ValueError(
                "Pattern mode must be either 'split' or 'extract'.")
        if self.include_delim is not None and self.include_delim not in ["prev", "next"]:
            raise ValueError(
                "Include delim must be either 'prev', 'next', or None.")
        if self.delimiters is not None and not isinstance(self.delimiters, (str, list)):
            raise ValueError(
                "Delimiters must be a string, list of strings, or None.")
        if isinstance(self.delimiters, list) and not all(isinstance(d, str) for d in self.delimiters):
            raise ValueError("All delimiters must be strings.")

    def __post_init__(self) -> None:
        '''Validate attributes.'''
        self._validate_fields()

    def __repr__(self) -> str:
        '''Return a string representation of the RecursiveLevel.'''
        return f"RecursiveLevel(whitespace={self.whitespace}, delimiters={self.delimiters}, include_delim={self.include_delim}, pattern={self.pattern}, pattern_mode={self.pattern_mode})"

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
        return cls(
            whitespace=data.get("whitespace", False),
            delimiters=data.get("delimiters"),
            include_delim=data.get("include_delim"),
            pattern=data.get("pattern"),
            pattern_mode=data.get("pattern_mode", "split")
        )

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
        # Placeholder for actual implementation
        # This would involve fetching the recipe from the Chonkie Recipe Store
        # and then creating the RecursiveLevel object from the recipe data
        raise NotImplementedError("This method is not implemented yet.")
