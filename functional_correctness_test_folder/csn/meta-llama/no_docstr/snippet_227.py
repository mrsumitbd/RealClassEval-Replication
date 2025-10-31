
from dataclasses import dataclass
import yaml


@dataclass
class TemplateFile:
    template: str
    params: dict

    def save(self, file_name: str):
        data = {
            'template': self.template,
            'params': self.params
        }
        with open(file_name, 'w') as file:
            yaml.dump(data, file)

    @classmethod
    def from_file(cls, file_name: str):
        try:
            with open(file_name, 'r') as file:
                data = yaml.safe_load(file)
                if data is None:
                    raise FileNotFoundError(f"File {file_name} is empty")
                return cls(**data)
        except FileNotFoundError:
            raise FileNotFoundError(f"File {file_name} not found")
        except yaml.YAMLError as e:
            raise ValueError(f"Failed to parse YAML in file {file_name}: {e}")
        except TypeError as e:
            raise ValueError(f"Invalid data in file {file_name}: {e}")
