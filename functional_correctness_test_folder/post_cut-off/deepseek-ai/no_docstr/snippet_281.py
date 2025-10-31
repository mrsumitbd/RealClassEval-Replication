
from typing import List, Dict, Any


class FewShotFormat:

    @staticmethod
    def convert(examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        formatted_examples = []
        for example in examples:
            formatted_example = {
                "input": str(example.get("input", "")),
                "output": str(example.get("output", ""))
            }
            formatted_examples.append(formatted_example)
        return formatted_examples

    @staticmethod
    def validate(examples: List[Dict[str, Any]]) -> bool:
        required_keys = {"input", "output"}
        for example in examples:
            if not isinstance(example, dict):
                return False
            if not required_keys.issubset(example.keys()):
                return False
            if not isinstance(example.get("input"), str) or not isinstance(example.get("output"), str):
                return False
        return True
