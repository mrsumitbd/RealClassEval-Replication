
import re
from typing import Dict, Any


class PromptPatternMatcher:
    '''Analyzes prompts to determine context requirements.'''

    def __init__(self):
        '''Initialize pattern matchers.'''
        self.patterns = {
            'time': re.compile(r'\b(time|date|year|month|day|hour|minute|second)\b', re.IGNORECASE),
            'location': re.compile(r'\b(location|place|city|country|address|geography)\b', re.IGNORECASE),
            'personal_info': re.compile(r'\b(name|email|phone|address|contact)\b', re.IGNORECASE),
            'financial': re.compile(r'\b(money|price|cost|budget|finance|account|transaction)\b', re.IGNORECASE),
            'technical': re.compile(r'\b(code|programming|software|hardware|algorithm|API|debug)\b', re.IGNORECASE),
            'medical': re.compile(r'\b(health|medical|doctor|hospital|disease|treatment)\b', re.IGNORECASE),
            'legal': re.compile(r'\b(law|legal|contract|lawyer|court|regulation)\b', re.IGNORECASE)
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
            'confidence': 0.0,
            'tool_name': tool_name,
            'arguments': arguments
        }

        for pattern_name, pattern in self.patterns.items():
            if pattern.search(prompt):
                results['patterns'].append(pattern_name)
                results['entities'].append(pattern_name)
                results['confidence'] += 0.1

        if results['patterns']:
            results['confidence'] = min(results['confidence'], 1.0)

        return results
