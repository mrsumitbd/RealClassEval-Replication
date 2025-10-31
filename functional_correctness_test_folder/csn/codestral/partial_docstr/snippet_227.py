
from dataclasses import dataclass


@dataclass
class TemplateFile:

    def save(self, file_name: str):
        with open(file_name, 'w') as file:
            file.write(str(self))

    @classmethod
    def from_file(cls, file_name: str):
        with open(file_name, 'r') as file:
            contents = file.read()
        return cls(contents)
