from typing import Any
from abc import abstractmethod
from dataclasses import dataclass

@dataclass
class RuleOption:
    """Base class representing a configurable part (i.e. option) of a rule (e.g. the max-length of the title-max-line
    rule).
    This class should not be used directly. Instead, use on the derived classes like StrOption, IntOption to set
    options of a particular type like int, str, etc.
    """
    name: str
    value: Any
    description: str

    def __post_init__(self):
        self.set(self.value)

    @abstractmethod
    def set(self, value: Any) -> None:
        """Validates and sets the option's value"""

    def __str__(self):
        return f'({self.name}: {self.value} ({self.description}))'