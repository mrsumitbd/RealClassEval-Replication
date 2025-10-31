
from typing import List, Dict, Any


class FewShotFormat:
    '''Handler for different few-shot example formats'''
    @staticmethod
    def convert(examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        converted_examples = []
        for example in examples:
            converted_example = {k: str(v) for k, v in example.items()}
            converted_examples.append(converted_example)
        return converted_examples

    @staticmethod
    def validate(examples: List[Dict[str, Any]]) -> bool:
        if not isinstance(examples, list):
            return False
        for example in examples:
            if not isinstance(example, dict):
                return False
            for k, v in example.items():
                if not isinstance(k, str):
                    return False
        return True
