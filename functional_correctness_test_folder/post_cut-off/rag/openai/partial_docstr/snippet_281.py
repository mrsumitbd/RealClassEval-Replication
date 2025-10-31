
from __future__ import annotations

from typing import Any, Dict, List, Tuple


class FewShotFormat:
    """Handler for different few-shot example formats."""

    # Mapping of alternative key names to the canonical 'input'/'output' pair.
    _ALTERNATE_KEYS: List[Tuple[List[str], List[str]]] = [
        (["prompt", "completion"], ["input", "output"]),
        (["question", "answer"], ["input", "output"]),
        (["text", "label"], ["input", "output"]),
        (["input_text", "output_text"], ["input", "output"]),
    ]

    @staticmethod
    def _convert_single(example: Dict[str, Any]) -> Dict[str, str]:
        """
        Convert a single example dict to the canonical {'input': str, 'output': str} format.
        Raises ValueError if conversion is not possible.
        """
        # If already canonical
        if "input" in example and "output" in example:
            inp = example["input"]
            out = example["output"]
            if not isinstance(inp, str) or not isinstance(out, str):
                raise ValueError(
                    f"Example has non-string 'input' or 'output': {example}"
                )
            return {"input": inp, "output": out}

        # Try alternate key pairs
        for src_keys, tgt_keys in FewShotFormat._ALTERNATE_KEYS:
            if all(k in example for k in src_keys):
                inp = example[src_keys[0]]
                out = example[src_keys[1]]
                if not isinstance(inp, str) or not isinstance(out, str):
                    raise ValueError(
                        f"Example has non-string values for keys {src_keys}: {example}"
                    )
                return {"input": inp, "output": out}

        # If example has a single key, treat it as both input and output
        if len(example) == 1:
            key, value = next(iter(example.items()))
            if not isinstance(value, str):
                raise ValueError(
                    f"Example single key value is not a string: {example}"
                )
            return {"input": value, "output": value}

        raise ValueError(f"Unsupported example format: {example}")

    @staticmethod
    def convert(examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Convert any supported format to the canonical input-output format.

        Parameters
        ----------
        examples : List[Dict[str, Any]]
            List of example dictionaries in any supported format.

        Returns
        -------
        List[Dict[str, str]]
            List of dictionaries each containing 'input' and 'output' keys with string values.
        """
        if not isinstance(examples, list):
            raise TypeError("examples must be a list of dictionaries")

        converted: List[Dict[str, str]] = []
        for idx, ex in enumerate(examples):
            if not isinstance(ex, dict):
                raise TypeError(f"Example at index {idx} is not a dict: {ex}")
            converted.append(FewShotFormat._convert_single(ex))
        return converted

    @staticmethod
    def validate(examples: List[Dict[str, Any]]) -> bool:
        """
        Validate that examples are already in the canonical input-output format.

        Parameters
        ----------
        examples : List[Dict[str, Any]]
            List of example dictionaries.

        Returns
        -------
        bool
            True if all examples contain 'input' and 'output' keys with string values, False otherwise.
        """
        if not isinstance(examples, list):
            return False
        for ex in examples:
            if not isinstance(ex, dict):
                return False
            if "input" not in ex or "output" not in ex:
                return False
            if not isinstance(ex["input"], str) or not isinstance(ex["output"], str):
                return False
        return True
