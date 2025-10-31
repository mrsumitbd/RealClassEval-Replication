from typing import Dict, List, Optional, Tuple

class TagInfo:

    def __init__(self, name: Optional[str], attrs: Dict[str, Optional[str]]) -> None:
        super().__init__()
        self._name = name
        self._attrs = attrs

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def attrs(self) -> Dict[str, Optional[str]]:
        return self._attrs