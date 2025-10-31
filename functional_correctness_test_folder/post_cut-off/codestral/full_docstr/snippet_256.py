
import re
from typing import Dict, Any


class PromptPatternMatcher:
    '''Analyzes prompts to determine context requirements.'''

    def __init__(self):
        '''Initialize pattern matchers.'''
        self.patterns = {
            'greeting': re.compile(r'\b(hello|hi|hey|greetings)\b', re.IGNORECASE),
            'goodbye': re.compile(r'\b(goodbye|bye|see you|farewell)\b', re.IGNORECASE),
            'question': re.compile(r'\b(what|when|where|who|why|how)\b', re.IGNORECASE),
            'statement': re.compile(r'\b(is|are|was|were|am)\b', re.IGNORECASE),
            'command': re.compile(r'\b(please|can you|could you|do you)\b', re.IGNORECASE),
        }

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Analyze prompt to determine context requirements.
        Returns:
            Dictionary with detected patterns, entities, and confidence scores
        '''
        results = {
            'patterns': [],
            'entities': [],
            'confidence': 0.0
        }

        for pattern_name, pattern in self.patterns.items():
            if pattern.search(prompt):
                results['patterns'].append(pattern_name)

        if tool_name:
            results['entities'].append(tool_name)

        if arguments:
            results['entities'].extend(arguments.keys())

        if results['patterns']:
            results['confidence'] = len(
                results['patterns']) / len(self.patterns)

        return results
