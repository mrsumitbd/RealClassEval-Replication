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
            # OpenAI format: {'role': 'user', 'content': ...}, {'role': 'assistant', 'content': ...}
            elif 'messages' in ex and isinstance(ex['messages'], list):
                user_msg = next(
                    (m['content'] for m in ex['messages'] if m.get('role') == 'user'), '')
                assistant_msg = next(
                    (m['content'] for m in ex['messages'] if m.get('role') == 'assistant'), '')
                converted.append(
                    {'input': str(user_msg), 'output': str(assistant_msg)})
            # Alpaca format: {'instruction': ..., 'input': ..., 'output': ...}
            elif 'instruction' in ex and 'output' in ex:
                inp = ex.get('input', '')
                instruction = ex['instruction']
                full_input = instruction if not inp else f"{instruction}\n{inp}"
                converted.append(
                    {'input': str(full_input), 'output': str(ex['output'])})
            # Vicuna format: {'conversations': [{'from': 'human', 'value': ...}, {'from': 'gpt', 'value': ...}]}
            elif 'conversations' in ex and isinstance(ex['conversations'], list):
                human = next(
                    (c['value'] for c in ex['conversations'] if c.get('from') == 'human'), '')
                gpt = next((c['value'] for c in ex['conversations']
                           if c.get('from') == 'gpt'), '')
                converted.append({'input': str(human), 'output': str(gpt)})
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
