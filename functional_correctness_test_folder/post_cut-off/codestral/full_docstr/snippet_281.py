
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
                    "Unsupported format. Each example must contain either 'input' and 'output', 'question' and 'answer', or 'prompt' and 'response'.")
        return converted_examples

    @staticmethod
    def validate(examples: List[Dict[str, Any]]) -> bool:
        '''Validate that examples are in input-output format'''
        for example in examples:
            if not ('input' in example and 'output' in example):
                return False
        return True
