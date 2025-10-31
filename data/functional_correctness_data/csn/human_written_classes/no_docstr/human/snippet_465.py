from typing import Any, Dict, List, Optional, Pattern

class AthenaTableMetadataColumn:

    def __init__(self, response):
        self._name: Optional[str] = response.get('Name')
        self._type: Optional[str] = response.get('Type')
        self._comment: Optional[str] = response.get('Comment')

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def type(self) -> Optional[str]:
        return self._type

    @property
    def comment(self) -> Optional[str]:
        return self._comment