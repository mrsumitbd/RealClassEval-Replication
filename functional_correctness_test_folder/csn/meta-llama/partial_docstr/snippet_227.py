
from dataclasses import dataclass
import json


@dataclass
class TemplateFile:
    contents: str

    def save(self, file_name: str):
        with open(file_name, 'w') as file:
            json.dump({'contents': self.contents}, file)

    @classmethod
    def from_file(cls, file_name: str):
        try:
            with open(file_name, 'r') as file:
                data = json.load(file)
                return cls(data['contents'])
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{file_name}' not found.")
        except json.JSONDecodeError:
            raise ValueError(f"File '{file_name}' is not a valid JSON file.")
        except KeyError:
            raise ValueError(f"File '{file_name}' is missing 'contents' key.")
