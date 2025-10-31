from typing import Any, Dict, List, Optional
from collections import defaultdict

class IDGenerator:

    def __init__(self) -> None:
        self.id_counter = defaultdict(int)

    def get_id(self, id_type: str, id_name: Optional[str]=None) -> str:
        self.id_counter[id_type] += 1
        id_name = id_name or id_type
        return f'{id_name}_{self.id_counter[id_type]}'