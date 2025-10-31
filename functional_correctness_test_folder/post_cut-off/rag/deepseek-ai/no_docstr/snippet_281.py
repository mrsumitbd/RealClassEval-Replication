
from typing import List, Dict, Any


class FewShotFormat:
    '''Handler for different few-shot example formats'''
    @staticmethod
    def convert(examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        '''Convert any supported format to input-output format'''
        converted_examples = []
        for example in examples:
            if 'input' in example and 'output' in example:
                converted_examples.append(
                    {'input': str(example['input']), 'output': str(example['output'])})
            elif 'context' in example and 'completion' in example:
                converted_examples.append(
                    {'input': str(example['context']), 'output': str(example['completion'])})
            elif 'question' in example and 'answer' in example:
                converted_examples.append(
                    {'input': str(example['question']), 'output': str(example['answer'])})
            else:
                raise ValueError(f"Unsupported example format: {example}")
        return converted_examples

    @staticmethod
    def validate(examples: List[Dict[str, Any]]) -> bool:
        '''Validate that examples are in input-output format'''
        for example in examples:
            if not isinstance(example, dict):
                return False
            if 'input' not in example or 'output' not in example:
                return False
            if not isinstance(example['input'], str) or not isinstance(example['output'], str):
                return False
        return True
