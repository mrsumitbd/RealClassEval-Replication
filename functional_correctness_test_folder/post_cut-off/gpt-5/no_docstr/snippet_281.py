from typing import Any, Dict, List


class FewShotFormat:
    _INPUT_KEYS = ("input", "prompt", "question", "source", "x")
    _OUTPUT_KEYS = ("output", "completion", "answer",
                    "target", "response", "y")

    @staticmethod
    def _pick_first_key(d: Dict[str, Any], keys: tuple) -> str:
        for k in keys:
            if k in d:
                v = d[k]
                if v is None:
                    continue
                s = str(v).strip()
                if s != "":
                    return s
        return ""

    @staticmethod
    def convert(examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        if not isinstance(examples, list):
            raise TypeError("examples must be a list of dicts")
        converted: List[Dict[str, str]] = []
        for i, ex in enumerate(examples):
            if not isinstance(ex, dict):
                raise TypeError(f"example at index {i} is not a dict")
            inp = FewShotFormat._pick_first_key(ex, FewShotFormat._INPUT_KEYS)
            out = FewShotFormat._pick_first_key(ex, FewShotFormat._OUTPUT_KEYS)
            if not inp or not out:
                raise ValueError(
                    f"example at index {i} must contain non-empty input and output fields"
                )
            converted.append({"input": inp, "output": out})
        return converted

    @staticmethod
    def validate(examples: List[Dict[str, Any]]) -> bool:
        if not isinstance(examples, list) or len(examples) == 0:
            return False
        for ex in examples:
            if not isinstance(ex, dict):
                return False
            inp = FewShotFormat._pick_first_key(ex, FewShotFormat._INPUT_KEYS)
            out = FewShotFormat._pick_first_key(ex, FewShotFormat._OUTPUT_KEYS)
            if not inp or not out:
                return False
        return True
