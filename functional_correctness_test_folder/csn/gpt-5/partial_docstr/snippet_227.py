from dataclasses import dataclass
from pathlib import Path


@dataclass
class TemplateFile:
    content: str = ""

    def save(self, file_name: str):
        path = Path(file_name)
        if path.parent:
            path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.content, encoding="utf-8")

    @classmethod
    def from_file(cls, file_name: str):
        '''
        read contents from a file
        :param cls:
        :type cls:
        :param file_name:
        :type file_name: str
        :returns:
        '''
        content = Path(file_name).read_text(encoding="utf-8")
        return cls(content=content)
