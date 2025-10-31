
from typing import List, Dict, Any


class FewShotFormat:
    '''Handler for different few-shot example formats'''
    @staticmethod
    def convert(examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Converts a list of examples into a standardized format.

        Args:
        examples (List[Dict[str, Any]]): A list of dictionaries containing examples.

        Returns:
        List[Dict[str, str]]: A list of dictionaries with 'input' and 'output' keys.
        """
        converted_examples = []
        for example in examples:
            input_text = str(example.get('input', ''))
            output_text = str(example.get('output', ''))
            converted_examples.append(
                {'input': input_text, 'output': output_text})
        return converted_examples

    @staticmethod
    def validate(examples: List[Dict[str, Any]]) -> bool:
        """
        Validates a list of examples.

        Args:
        examples (List[Dict[str, Any]]): A list of dictionaries containing examples.

        Returns:
        bool: True if all examples are valid, False otherwise.
        """
        for example in examples:
            if not isinstance(example, dict):
                return False
            if 'input' not in example or 'output' not in example:
                return False
            if not isinstance(example['input'], str) or not isinstance(example['output'], str):
                return False
        return True
