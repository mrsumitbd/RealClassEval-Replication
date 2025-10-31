
from typing import List, Dict, Any


class FewShotFormat:

    @staticmethod
    def convert(examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        result = []
        for ex in examples:
            input_str = str(ex.get("input", ""))
            output_str = str(ex.get("output", ""))
            result.append({"input": input_str, "output": output_str})
        return result

    @staticmethod
    def validate(examples: List[Dict[str, Any]]) -> bool:
        if not isinstance(examples, list):
            return False
        for ex in examples:
            if not isinstance(ex, dict):
                return False
            if "input" not in ex or "output" not in ex:
                return False
        return True
