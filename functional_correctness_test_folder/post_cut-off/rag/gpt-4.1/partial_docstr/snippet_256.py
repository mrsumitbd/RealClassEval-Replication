import re
from typing import Any, Dict, List


class PromptPatternMatcher:
    '''Analyzes prompts to determine context requirements.'''

    def __init__(self):
        '''Initialize pattern matchers.'''
        # Define some example patterns for context requirements
        self.patterns = [
            {
                'name': 'requires_file',
                'regex': re.compile(r'\b(file|document|upload|attachment)\b', re.IGNORECASE),
                'entity': 'file'
            },
            {
                'name': 'requires_user',
                'regex': re.compile(r'\b(user|username|account|profile)\b', re.IGNORECASE),
                'entity': 'user'
            },
            {
                'name': 'requires_date',
                'regex': re.compile(r'\b(date|time|when|schedule|deadline)\b', re.IGNORECASE),
                'entity': 'date'
            },
            {
                'name': 'requires_location',
                'regex': re.compile(r'\b(location|address|place|where|city|country)\b', re.IGNORECASE),
                'entity': 'location'
            },
            {
                'name': 'requires_email',
                'regex': re.compile(r'\b(email|mail|e-mail)\b', re.IGNORECASE),
                'entity': 'email'
            },
        ]

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Analyze prompt to determine context requirements.
        Returns:
            Dictionary with detected patterns, entities, and confidence scores
        '''
        detected_patterns: List[Dict[str, Any]] = []
        entities: List[str] = []
        confidence_scores: Dict[str, float] = {}

        for pattern in self.patterns:
            matches = pattern['regex'].findall(prompt)
            if matches:
                detected_patterns.append({
                    'pattern': pattern['name'],
                    'matches': matches
                })
                entities.append(pattern['entity'])
                # Confidence: simple heuristic, more matches = higher confidence
                confidence_scores[pattern['entity']] = min(
                    1.0, 0.5 + 0.1 * len(matches))

        # Optionally, check arguments for additional context clues
        for arg_key in arguments:
            for pattern in self.patterns:
                if pattern['entity'] in arg_key.lower() and pattern['entity'] not in entities:
                    entities.append(pattern['entity'])
                    detected_patterns.append({
                        'pattern': pattern['name'],
                        'matches': [arg_key]
                    })
                    confidence_scores[pattern['entity']] = 0.7

        result = {
            'detected_patterns': detected_patterns,
            'entities': list(set(entities)),
            'confidence_scores': confidence_scores
        }
        return result
