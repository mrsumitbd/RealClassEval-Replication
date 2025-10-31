from typing import Any
from dataclasses import dataclass

@dataclass
class APIResponse:

    @staticmethod
    def success(data: Any=None, message: str='success') -> dict:
        return {'code': 0, 'message': message, 'data': data}

    @staticmethod
    def error(message: str, code: int=1, data: Any=None) -> dict:
        return {'code': code, 'message': message, 'data': data}