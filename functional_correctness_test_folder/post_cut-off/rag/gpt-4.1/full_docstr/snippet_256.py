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
                'name': 'requires_user_info',
                'regex': re.compile(r'\b(user|profile|account|login|email|username)\b', re.IGNORECASE),
                'entity': 'user_info'
            },
            {
                'name': 'requires_date',
                'regex': re.compile(r'\b(date|time|schedule|calendar|appointment)\b', re.IGNORECASE),
                'entity': 'date'
            },
            {
                'name': 'requires_location',
                'regex': re.compile(r'\b(location|address|city|country|place|where)\b', re.IGNORECASE),
                'entity': 'location'
            },
            {
                'name': 'requires_confirmation',
                'regex': re.compile(r'\b(confirm|confirmation|sure|are you sure|verify)\b', re.IGNORECASE),
                'entity': 'confirmation'
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
                # Confidence: number of matches / 3, capped at 1.0
                confidence = min(len(matches) / 3.0, 1.0)
                confidence_scores[pattern['entity']] = confidence

        # Optionally, boost confidence if argument keys match entities
        for entity in entities:
            if entity in arguments:
                confidence_scores[entity] = max(
                    confidence_scores.get(entity, 0.0), 0.9)

        result = {
            'detected_patterns': detected_patterns,
            'entities': list(set(entities)),
            'confidence_scores': confidence_scores,
            'tool_name': tool_name
        }
        return result
