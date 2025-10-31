from typing import Any, Callable, Dict, List

class Parameter:

    def __init__(self, name: str, description: str, type_: str, required: bool=True):
        self.name = name
        self.description = description
        self.type = type_
        self.required = required
        self.value = None

    def get_descriptor_json(self) -> Dict:
        return {'description': self.description, 'type': self.type}

    def set_value(self, value: Any):
        self.value = value

    def get_value(self) -> Any:
        return self.value