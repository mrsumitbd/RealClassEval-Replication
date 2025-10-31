
from dataclasses import dataclass


@dataclass
class TemplateFile:
    content: str = ""

    def save(self, file_name: str):
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(self.content)

    @classmethod
    def from_file(cls, file_name: str):
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read()
        return cls(content=content)
