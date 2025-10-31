
from __future__ import annotations

from typing import Any, Dict, List


class FewShotFormat:
    """Handler for different few‑shot example formats."""

    @staticmethod
    def convert(examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Convert any supported format to the canonical input‑output format.

        Supported source formats (key pairs) are:
            - {'input': ..., 'output': ...}
            - {'prompt': ..., 'completion': ...}
            - {'question': ..., 'answer': ...}
            - {'text': ..., 'label': ...}

        The returned list contains dictionaries with keys ``input`` and ``output``
        whose values are strings.  Non‑string values are coerced to ``str``.
        """
        canonical: List[Dict[str, str]] = []

        for idx, ex in enumerate(examples):
            if not isinstance(ex, dict):
                raise ValueError(
                    f"Example at index {idx} is not a dict: {ex!r}")

            # Helper to coerce to string
            def _str(v: Any) -> str:
                return str(v) if v is not None else ""

            # Detect format
            if "input" in ex and "output" in ex:
                inp, out = ex["input"], ex["output"]
            elif "prompt" in ex and "completion" in ex:
                inp, out = ex["prompt"], ex["completion"]
            elif "question" in ex and "answer" in ex:
                inp, out = ex["question"], ex["answer"]
            elif "text" in ex and "label" in ex:
                inp, out = ex["text"], ex["label"]
            else:
                raise ValueError(
                    f"Unsupported example format at index {idx}: {ex!r}"
                )

            canonical.append({"input": _str(inp), "output": _str(out)})

        return canonical

    @staticmethod
    def validate(examples: List[Dict[str, Any]]) -> bool:
        """
        Validate that all examples are already in the canonical input‑output format.

        Returns ``True`` if every example is a dictionary containing the keys
        ``input`` and ``output`` and both values are strings.  Otherwise returns
        ``False``.
        """
        for idx, ex in enumerate(examples):
            if not isinstance(ex, dict):
                return False
            if "input" not in ex or "output" not in ex:
                return False
            if not isinstance(ex["input"], str) or not isinstance(ex["output"], str):
                return False
        return True
