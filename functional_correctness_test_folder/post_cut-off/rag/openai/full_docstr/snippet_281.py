
from __future__ import annotations

from typing import Any, Dict, List


class FewShotFormat:
    """Handler for different few-shot example formats."""

    @staticmethod
    def convert(examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Convert any supported format to input-output format.

        Supported input formats:
            - {'input': ..., 'output': ...}
            - {'prompt': ..., 'response': ...}
            - {'question': ..., 'answer': ...}
            - {'text': ..., 'label': ...}
            - {'input_text': ..., 'output_text': ...}

        Returns a list of dictionaries with keys 'input' and 'output'.
        Raises ValueError if an example cannot be converted.
        """
        converted: List[Dict[str, str]] = []

        for idx, example in enumerate(examples):
            if not isinstance(example, dict):
                raise ValueError(
                    f"Example at index {idx} is not a dict: {example!r}")

            # Direct input-output
            if "input" in example and "output" in example:
                inp = example["input"]
                out = example["output"]
            # Prompt-response
            elif "prompt" in example and "response" in example:
                inp = example["prompt"]
                out = example["response"]
            # Question-answer
            elif "question" in example and "answer" in example:
                inp = example["question"]
                out = example["answer"]
            # Text-label
            elif "text" in example and "label" in example:
                inp = example["text"]
                out = example["label"]
            # Input_text-output_text
            elif "input_text" in example and "output_text" in example:
                inp = example["input_text"]
                out = example["output_text"]
            else:
                raise ValueError(
                    f"Example at index {idx} does not match any supported format: {example!r}"
                )

            # Ensure both are strings
            if not isinstance(inp, str) or not isinstance(out, str):
                raise ValueError(
                    f"Example at index {idx} has non-string input/output: input={inp!r}, output={out!r}"
                )

            converted.append({"input": inp, "output": out})

        return converted

    @staticmethod
    def validate(examples: List[Dict[str, Any]]) -> bool:
        """
        Validate that examples are in input-output format.

        Returns True if every example is a dict containing string 'input' and 'output' keys.
        """
        for idx, example in enumerate(examples):
            if not isinstance(example, dict):
                return False
            if "input" not in example or "output" not in example:
                return False
            if not isinstance(example["input"], str) or not isinstance(example["output"], str):
                return False
        return True
