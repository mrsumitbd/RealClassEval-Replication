from typing import Dict

class KeyMapper:

    def __init__(self, to_trinity_map: Dict[str, str]):
        self.to_trinity_map = to_trinity_map
        self.from_trinity_map = {v: k for k, v in self.to_trinity_map.items()}

    def to_trinity(self, key: str) -> str:
        return self.to_trinity_map.get(key, key)

    def from_trinity(self, key: str) -> str:
        return self.from_trinity_map.get(key, key)