from typing import Set, Optional, Dict, Any, List

class FewShotFormat:
    """Handler for different few-shot example formats"""

    @staticmethod
    def convert(examples: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Convert any supported format to input-output format"""
        if not examples:
            return []
        if all((isinstance(ex, dict) and 'input' in ex and ('output' in ex) for ex in examples)):
            return examples
        if all((isinstance(ex, dict) and 'role' in ex for ex in examples)):
            return [{'input': examples[i]['content'][0]['text'], 'output': examples[i + 1]['content'][0]['text']} for i in range(0, len(examples), 2) if i + 1 < len(examples) and examples[i]['role'] == 'user' and (examples[i + 1]['role'] == 'assistant')]
        raise ValueError('Unsupported example format')

    @staticmethod
    def validate(examples: List[Dict[str, Any]]) -> bool:
        """Validate that examples are in input-output format"""
        return all((isinstance(ex, dict) and 'input' in ex and ('output' in ex) and isinstance(ex['input'], str) and isinstance(ex['output'], str) for ex in examples))