from typing import Callable, Iterator, List, Optional
from collections import Counter

class GenericColumnMapper:

    def __init__(self):
        self.call_counts = Counter()

    def _short_circuit(self, column_name: str) -> Optional[str]:
        return None

    def map_list(self, column_names: List[str]) -> Iterator[str]:
        self.call_counts = Counter()
        for column_name in column_names:
            yield self.map(str(column_name))

    def map(self, column_name: str) -> str:
        self.call_counts[column_name] += 1
        if self.call_counts[column_name] == 1:
            return column_name
        munged_value = self._short_circuit(column_name)
        return munged_value if munged_value is not None else f'{column_name} {self.call_counts[column_name]}'