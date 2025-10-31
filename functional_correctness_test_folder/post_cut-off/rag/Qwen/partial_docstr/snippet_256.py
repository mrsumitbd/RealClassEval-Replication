
import re
from typing import Any, Dict, List


class PromptPatternMatcher:
    '''Analyzes prompts to determine context requirements.'''

    def __init__(self):
        '''Initialize pattern matchers.'''
        self.patterns = {
            'greeting': r'\b(hello|hi|hey)\b',
            'farewell': r'\b(goodbye|bye|see you)\b',
            'question': r'\b(what|how|why|when|where|who)\b',
            'request': r'\bplease\b',
            'tool_invocation': r'\buse the {tool_name}\b'
        }

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Analyze prompt to determine context requirements.
        Returns:
            Dictionary with detected patterns, entities, and confidence scores
        '''
        results = {
            'patterns': {},
            'entities': {},
            'confidence': 0.0
        }

        for pattern_name, pattern in self.patterns.items():
            pattern = pattern.format(tool_name=tool_name)
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                results['patterns'][pattern_name] = match.group()
                results['confidence'] += 0.25

        # Extract entities based on arguments
        for arg_name, arg_value in arguments.items():
            if isinstance(arg_value, str):
                if re.search(re.escape(arg_value), prompt, re.IGNORECASE):
                    results['entities'][arg_name] = arg_value
                    results['confidence'] += 0.25

        return results
