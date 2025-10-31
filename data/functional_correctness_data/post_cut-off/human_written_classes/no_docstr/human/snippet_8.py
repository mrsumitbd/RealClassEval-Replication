import logging
from typing import Any, Dict, List, Optional, Union

class ShadeMergeResponse:

    def __init__(self, result: Any, success: bool):
        self.success: bool = success
        self.message: str = ''
        self.merge_shade_list: Optional[List[Dict[str, Any]]] = None
        if not success:
            self.message = result if isinstance(result, str) else 'Error occurred'
            logging.error(self.message)
        else:
            self.message = 'Success'
            self.merge_shade_list = result.get('mergeShadeList')

    def to_json(self) -> dict:
        return {'success': self.success, 'message': self.message, 'mergeShadeList': self.merge_shade_list}