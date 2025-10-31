
from typing import List, Dict, Any


class FewShotFormat:
    """Handler for different few-shot example formats"""

    @staticmethod
    def convert(examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Convert any supported format to input-output format"""
        converted_examples = []
        for example in examples:
            if 'input' in example and 'output' in example:
                converted_examples.append(
                    {'input': str(example['input']), 'output': str(example['output'])})
            elif 'src' in example and 'tgt' in example:
                converted_examples.append(
                    {'input': str(example['src']), 'output': str(example['tgt'])})
            elif 'text' in example and 'summary' in example:
                converted_examples.append(
                    {'input': str(example['text']), 'output': str(example['summary'])})
            else:
                raise ValueError(f"Unsupported example format: {example}")
        return converted_examples

    @staticmethod
    def validate(examples: List[Dict[str, Any]]) -> bool:
        """Validate that examples are in input-output format"""
        for example in examples:
            if not isinstance(example, dict):
                return False
            if 'input' not in example or 'output' not in example:
                return False
            if not isinstance(example['input'], str) or not isinstance(example['output'], str):
                return False
        return True
