
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
                    {'input': example['input'], 'output': example['output']})
            elif 'question' in example and 'answer' in example:
                converted_examples.append(
                    {'input': example['question'], 'output': example['answer']})
            elif 'prompt' in example and 'response' in example:
                converted_examples.append(
                    {'input': example['prompt'], 'output': example['response']})
            else:
                raise ValueError(
                    'Unsupported example format. Expected keys: "input"/"output", "question"/"answer", or "prompt"/"response".')
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
