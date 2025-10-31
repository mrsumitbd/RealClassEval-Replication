
from typing import List, Dict, Any


class FewShotFormat:
    '''Handler for different few-shot example formats'''
    @staticmethod
    def convert(examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        converted = []
        for ex in examples:
            new_ex = {}
            for k, v in ex.items():
                new_ex[str(k)] = str(v)
            converted.append(new_ex)
        return converted

    @staticmethod
    def validate(examples: List[Dict[str, Any]]) -> bool:
        if not isinstance(examples, list):
            return False
        for ex in examples:
            if not isinstance(ex, dict):
                return False
            for k, v in ex.items():
                if not isinstance(k, str):
                    return False
                if not (isinstance(v, str) or isinstance(v, int) or isinstance(v, float) or v is None):
                    return False
        return True
