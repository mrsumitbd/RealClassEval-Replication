
from typing import List, Dict, Any


class FewShotFormat:
    '''Handler for different few-shot example formats'''
    @staticmethod
    def convert(examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        '''Convert any supported format to input-output format'''
        converted_examples = []
        for example in examples:
            if 'input' in example and 'output' in example:
                converted_example = {
                    'input': str(example['input']),
                    'output': str(example['output'])
                }
                converted_examples.append(converted_example)
            elif 'in' in example and 'out' in example:
                converted_example = {
                    'input': str(example['in']),
                    'output': str(example['out'])
                }
                converted_examples.append(converted_example)
        return converted_examples

    @staticmethod
    def validate(examples: List[Dict[str, Any]]) -> bool:
        '''Validate that examples are in input-output format'''
        for example in examples:
            if not ('input' in example and 'output' in example) and not ('in' in example and 'out' in example):
                return False
        return True
