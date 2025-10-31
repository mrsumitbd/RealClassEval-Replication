
from dataclasses import dataclass


@dataclass
class TemplateFile:
    content: str = ""

    def save(self, file_name: str):
        with open(file_name, 'w') as f:
            f.write(self.content)

    @classmethod
    def from_file(cls, file_name: str):
        with open(file_name, 'r') as f:
            content = f.read()
        return cls(content)
