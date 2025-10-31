
from typing import List, Dict, Any


class FewShotFormat:
    """Handler for different few‑shot example formats.

    The class expects each example to be a mapping containing at least the
    keys ``input`` and ``output``.  The :meth:`convert` method normalises the
    values to strings, while :meth:`validate` checks that the structure is
    correct.
    """

    @staticmethod
    def convert(examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Convert a list of example dictionaries into a list of dictionaries
        with string values for the ``input`` and ``output`` keys.

        Parameters
        ----------
        examples : List[Dict[str, Any]]
            A list of example dictionaries.  Each dictionary may contain
            arbitrary keys, but must contain ``input`` and ``output`` keys.

        Returns
        -------
        List[Dict[str, str]]
            A new list where each dictionary contains only the ``input`` and
            ``output`` keys, with their values converted to strings.

        Raises
        ------
        ValueError
            If any example is missing the required keys.
        """
        converted: List[Dict[str, str]] = []

        for idx, example in enumerate(examples):
            if not isinstance(example, dict):
                raise ValueError(f"Example at index {idx} is not a dict.")

            if "input" not in example or "output" not in example:
                raise ValueError(
                    f"Example at index {idx} must contain 'input' and 'output' keys."
                )

            # Convert values to strings; preserve None as empty string
            inp = "" if example["input"] is None else str(example["input"])
            out = "" if example["output"] is None else str(example["output"])

            converted.append({"input": inp, "output": out})

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
            ``True`` if every example is a dictionary containing the keys
            ``input`` and ``output``; otherwise ``False``.
        """
        if not isinstance(examples, list):
            return False

        for idx, example in enumerate(examples):
            if not isinstance(example, dict):
                return False
            if "input" not in example or "output" not in example:
                return False

        return True
