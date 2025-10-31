
from typing import List, Dict, Any


class FewShotFormat:

    @staticmethod
    def convert(examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Converts a list of examples into a few-shot format.

        Args:
        examples (List[Dict[str, Any]]): A list of examples where each example is a dictionary.

        Returns:
        List[Dict[str, str]]: A list of examples in few-shot format.
        """
        few_shot_examples = []
        for example in examples:
            input_text = ""
            output_text = ""
            for key, value in example.items():
                if key.startswith("input"):
                    input_text += f"{key}: {value}\n"
                elif key.startswith("output"):
                    output_text += f"{value}"
            few_shot_example = {
                "input": input_text.strip(),
                "output": output_text.strip()
            }
            few_shot_examples.append(few_shot_example)
        return few_shot_examples

    @staticmethod
    def validate(examples: List[Dict[str, Any]]) -> bool:
        """
        Validates if the given examples are in the correct format for few-shot learning.

        Args:
        examples (List[Dict[str, Any]]): A list of examples where each example is a dictionary.

        Returns:
        bool: True if the examples are valid, False otherwise.
        """
        for example in examples:
            has_input = False
            has_output = False
            for key in example.keys():
                if key.startswith("input"):
                    has_input = True
                elif key.startswith("output"):
                    has_output = True
            if not (has_input and has_output):
                return False
        return True
