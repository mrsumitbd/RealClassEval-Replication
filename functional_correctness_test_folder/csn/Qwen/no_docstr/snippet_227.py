
from dataclasses import dataclass
import json


@dataclass
class TemplateFile:
    content: str

    def save(self, file_name: str):
        with open(file_name, 'w') as file:
            json.dump(self.content, file)

    @classmethod
    def from_file(cls, file_name: str):
        with open(file_name, 'r') as file:
            content = json.load(file)
        return cls(content=content)
