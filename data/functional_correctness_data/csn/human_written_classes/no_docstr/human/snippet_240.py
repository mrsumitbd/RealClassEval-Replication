from typing import Dict

class Remapped:

    def __init__(self, mapping: Dict[str, str], *args, **kwargs):
        self._reversed_mapping = {value: key for key, value in mapping.items()}
        super().__init__(*args, **kwargs)

    def __getattr__(self, key):
        if key in self._reversed_mapping:
            return super().__getattr__(self._reversed_mapping[key])
        return super().__getattr__(key)