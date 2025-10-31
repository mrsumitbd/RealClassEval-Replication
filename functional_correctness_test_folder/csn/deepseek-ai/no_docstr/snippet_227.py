
from dataclasses import dataclass


@dataclass
class TemplateFile:
    def save(self, file_name: str):
        pass

    @classmethod
    def from_file(cls, file_name: str):
        pass
