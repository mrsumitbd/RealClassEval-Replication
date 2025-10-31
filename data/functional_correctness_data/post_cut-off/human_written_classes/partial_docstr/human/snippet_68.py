from dataclasses import dataclass
from typing import Literal, Tuple

@dataclass(frozen=True)
class IndentType:
    """Class representing indentation type with size attribute."""
    type: Literal['space', 'tab', 'mixed']
    size: int = 4
    most_used: 'IndentType | None' = None

    @property
    def is_tab(self) -> bool:
        return self.type == 'tab'

    @property
    def is_mixed(self) -> bool:
        return self.type == 'mixed'

    @property
    def is_space(self) -> bool:
        return self.type == 'space'

    @classmethod
    def space(cls, size: int=4) -> 'IndentType':
        """Create a space indentation type with the specified size."""
        return cls(type='space', size=size)

    @classmethod
    def tab(cls, size: int=1) -> 'IndentType':
        """Create a tab indentation type (size is typically 1)."""
        return cls(type='tab', size=size)

    @classmethod
    def mixed(cls, most_used: 'IndentType | None'=None) -> 'IndentType':
        """Create a mixed indentation type."""
        return cls(type='mixed', size=1, most_used=most_used)

    def __repr__(self):
        if self.is_mixed:
            most_used_str = f', most_used={self.most_used}' if self.most_used else ''
            return f'IndentType({self.type}{most_used_str})'
        if self.is_tab:
            return f'IndentType({self.type})'
        return f'IndentType({self.type}, size={self.size})'