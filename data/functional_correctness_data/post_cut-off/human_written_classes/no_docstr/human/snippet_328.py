from functools import cached_property
import re
from dataclasses import dataclass

@dataclass
class DataDependency:
    name: str
    version: str

    def __post_init__(self):
        self.name = re.sub('\\[.*\\]', '', self.name)
        self.name = self.name.replace('_', '-').strip()
        self.name = self.name.lower()
        self.version = self.version.strip()
        self.version = re.sub('\\.0$', '', self.version)

    @cached_property
    def pretty_name(self):
        return f'{self.name}=={self.version}'

    def __str__(self):
        return self.pretty_name
    __repr__ = __str__

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))