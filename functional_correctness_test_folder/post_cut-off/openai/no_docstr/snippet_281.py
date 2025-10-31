
from typing import Any, Dict, List


class FewShotFormat:
    """
    Utility class for converting and validating examples for few‑shot learning.
    Each example is expected to be a mapping containing at least the keys
    ``input`` and ``output``.  The ``convert`` method normalises the values
    to strings, while ``validate`` checks that the structure is correct.
    """

    @staticmethod
    def convert(examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Convert a list of example dictionaries into a list of dictionaries
        with string values for the ``input`` and ``output`` keys.

        Parameters
        ----------
        examples : List[Dict[str, Any]]
            A list of example dictionaries.  Each dictionary must contain
            the keys ``input`` and ``output``.

        Returns
        -------
        List[Dict[str, str]]
            A new list where each dictionary contains only the keys
            ``input`` and ``output`` with string values.

        Raises
        ------
        ValueError
            If any example is missing the required keys or if the values
            cannot be converted to strings.
        """
        converted: List[Dict[str, str]] = []

        for idx, example in enumerate(examples):
            if not isinstance(example, dict):
                raise ValueError(f"Example at index {idx} is not a dict.")

            if "input" not in example or "output" not in example:
                raise ValueError(
                    f"Example at index {idx} missing required 'input' or 'output' keys."
                )

            try:
                input_str = str(example["input"])
                output_str = str(example["output"])
            except Exception as exc:
                raise ValueError(
                    f"Could not convert 'input' or 'output' to string in example at index {idx}."
                ) from exc

            converted.append({"input": input_str, "output": output_str})

        return converted

    @staticmethod
    def validate(examples: List[Dict[str, Any]]) -> bool:
        """
        Validate that a list of examples conforms to the expected format.

        Parameters
        ----------
        examples : List[Dict[str, Any]]
            A list of example dictionaries.

        Returns
        -------
        bool
            ``True`` if all examples contain the required keys and the
            values can be converted to strings; otherwise ``False``.
        """
        try:
            # Reuse the conversion logic to perform validation.
            # If conversion succeeds for all examples, validation passes.
            _ = FewShotFormat.convert(examples)
            return True
        except Exception:
            return False
