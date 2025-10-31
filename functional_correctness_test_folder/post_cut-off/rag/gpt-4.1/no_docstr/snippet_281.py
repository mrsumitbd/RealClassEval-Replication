from typing import List, Dict, Any


class FewShotFormat:
    '''Handler for different few-shot example formats'''

    @staticmethod
    def convert(examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        '''Convert any supported format to input-output format'''
        converted = []
        for ex in examples:
            # If already in input-output format
            if 'input' in ex and 'output' in ex:
                converted.append(
                    {'input': str(ex['input']), 'output': str(ex['output'])})
            # OpenAI format: prompt-completion
            elif 'prompt' in ex and 'completion' in ex:
                converted.append(
                    {'input': str(ex['prompt']), 'output': str(ex['completion'])})
            # Alpaca format: instruction-input-output
            elif 'instruction' in ex and 'output' in ex:
                inp = ex.get('input', '')
                if inp:
                    input_str = f"{ex['instruction'].strip()}\n{inp.strip()}"
                else:
                    input_str = ex['instruction'].strip()
                converted.append(
                    {'input': input_str, 'output': str(ex['output'])})
            else:
                raise ValueError(f"Unsupported example format: {ex}")
        return converted

    @staticmethod
    def validate(examples: List[Dict[str, Any]]) -> bool:
        '''Validate that examples are in input-output format'''
        for ex in examples:
            if not isinstance(ex, dict):
                return False
            if 'input' not in ex or 'output' not in ex:
                return False
            if not isinstance(ex['input'], str) or not isinstance(ex['output'], str):
                return False
        return True
