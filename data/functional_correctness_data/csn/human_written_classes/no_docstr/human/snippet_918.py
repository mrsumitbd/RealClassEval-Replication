from cytomine.cytomine import Cytomine
from typing import Any, Dict, Optional, Union

class CytomineUser:

    def __init__(self) -> None:
        self.username: Optional[str] = None
        self.origin = None

    def keys(self) -> Optional[Union[bool, Dict[str, str]]]:
        if hasattr(self, 'id') and self.id:
            return Cytomine.get_instance().get(f'user/{self.id}/keys.json')
        return None