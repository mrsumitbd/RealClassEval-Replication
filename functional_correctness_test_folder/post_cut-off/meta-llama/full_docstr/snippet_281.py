
from typing import List, Dict, Any


class FewShotFormat:
    '''Handler for different few-shot example formats'''

    @staticmethod
    def convert(examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        '''Convert any supported format to input-output format'''
        # Check if examples are already in input-output format
        if FewShotFormat.validate(examples):
            return examples

        # Check if examples are in a supported alternative format
        if all('input' in ex and 'output' in ex for ex in examples):
            return [{'input': ex['input'], 'output': ex['output']} for ex in examples]
        elif all('text' in ex and 'label' in ex for ex in examples):
            return [{'input': ex['text'], 'output': ex['label']} for ex in examples]
        elif all('question' in ex and 'answer' in ex for ex in examples):
            return [{'input': ex['question'], 'output': ex['answer']} for ex in examples]
        else:
            raise ValueError("Unsupported format for few-shot examples")

    @staticmethod
    def validate(examples: List[Dict[str, Any]]) -> bool:
        '''Validate that examples are in input-output format'''
        return all(isinstance(ex, dict) and 'input' in ex and 'output' in ex
                   and isinstance(ex['input'], str) and isinstance(ex['output'], str)
                   for ex in examples)
