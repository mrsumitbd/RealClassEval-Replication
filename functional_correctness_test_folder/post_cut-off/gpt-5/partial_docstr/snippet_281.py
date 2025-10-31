from typing import Any, Dict, List, Optional, Tuple


class FewShotFormat:
    '''Handler for different few-shot example formats'''
    _INPUT_PRIORITY = ["input", "prompt", "question",
                       "source", "x", "instruction", "query"]
    _OUTPUT_PRIORITY = ["output", "completion",
                        "answer", "target", "y", "response", "label"]

    @staticmethod
    def _extract_io(example: Dict[str, Any]) -> Optional[Tuple[str, str]]:
        if not isinstance(example, dict):
            return None

        keys = set(example.keys())

        in_key = None
        out_key = None

        for k in FewShotFormat._INPUT_PRIORITY:
            if k in keys:
                in_key = k
                break
        for k in FewShotFormat._OUTPUT_PRIORITY:
            if k in keys:
                out_key = k
                break

        if in_key is None or out_key is None:
            return None

        in_val = example.get(in_key, None)
        out_val = example.get(out_key, None)

        if in_val is None or out_val is None:
            return None

        try:
            in_s = str(in_val)
            out_s = str(out_val)
        except Exception:
            return None

        return in_s, out_s

    @staticmethod
    def convert(examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        result: List[Dict[str, str]] = []
        for i, ex in enumerate(examples):
            pair = FewShotFormat._extract_io(ex)
            if pair is None:
                raise ValueError(
                    f"Example at index {i} cannot be converted to input/output format")
            inp, out = pair
            result.append({"input": inp, "output": out})
        return result

    @staticmethod
    def validate(examples: List[Dict[str, Any]]) -> bool:
        if not isinstance(examples, list):
            return False
        for ex in examples:
            pair = FewShotFormat._extract_io(ex)
            if pair is None:
                return False
            inp, out = pair
            if not isinstance(inp, str) or not isinstance(out, str):
                return False
            if inp == "" or out == "":
                return False
        return True
