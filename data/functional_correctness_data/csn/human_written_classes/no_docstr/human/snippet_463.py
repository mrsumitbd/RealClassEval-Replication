from typing import Any, Dict, List, Optional, Pattern
from pyathena.error import DataError

class AthenaDatabase:

    def __init__(self, response):
        database = response.get('Database')
        if not database:
            raise DataError('KeyError `Database`')
        self._name: Optional[str] = database.get('Name')
        self._description: Optional[str] = database.get('Description')
        self._parameters: Dict[str, str] = database.get('Parameters', {})

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def parameters(self) -> Dict[str, str]:
        return self._parameters