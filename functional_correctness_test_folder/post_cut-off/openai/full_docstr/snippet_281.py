
from typing import List, Dict, Any


class FewShotFormat:
    '''Handler for different few-shot example formats'''

    @staticmethod
    def convert(examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        '''Convert any supported format to input-output format'''
        if not isinstance(examples, list):
            raise TypeError("examples must be a list of dicts")

        converted: List[Dict[str, str]] = []

        for idx, ex in enumerate(examples):
            if not isinstance(ex, dict):
                raise TypeError(f"example at index {idx} is not a dict")

            # Already in desired format
            if 'input' in ex and 'output' in ex:
                inp, out = ex['input'], ex['output']
                if not isinstance(inp, str) or not isinstance(out, str):
                    raise ValueError(
                        f"example at index {idx} has non-string input/output")
                converted.append({'input': inp, 'output': out})
                continue

            # Common alternative key pairs
            key_map = [
                ('question', 'answer'),
                ('prompt', 'completion'),
                ('text', 'label'),
                ('input_text', 'output_text'),
                ('instruction', 'response'),
                ('prompt_text', 'completion_text'),
            ]

            found = False
            for in_key, out_key in key_map:
                if in_key in ex and out_key in ex:
                    inp, out = ex[in_key], ex[out_key]
                    if not isinstance(inp, str) or not isinstance(out, str):
                        raise ValueError(
                            f"example at index {idx} has non-string {in_key}/{out_key}")
                    converted.append({'input': inp, 'output': out})
                    found = True
                    break

            if not found:
                raise ValueError(
                    f"example at index {idx} does not match any supported format: {ex}"
                )

        return converted

    @staticmethod
    def validate(examples: List[Dict[str, Any]]) -> bool:
        '''Validate that examples are in input-output format'''
        if not isinstance(examples, list):
            return False

        for ex in examples:
            if not isinstance(ex, dict):
                return False
            if 'input' not in ex or 'output' not in ex:
                return False
            if not isinstance(ex['input'], str) or not isinstance(ex['output'], str):
                return False

        return True
