
import re
from typing import Dict, Any, List


class PromptPatternMatcher:
    '''Analyzes prompts to determine context requirements.'''

    def __init__(self):
        '''Initialize pattern matchers.'''
        # Define some example patterns for context requirements
        self.patterns = [
            {
                'name': 'requires_previous_context',
                'regex': re.compile(r'\b(as (before|previously|earlier|above|mentioned|discussed))\b', re.IGNORECASE),
                'confidence': 0.9
            },
            {
                'name': 'requires_user_info',
                'regex': re.compile(r'\b(my|user|account|profile|settings|preferences)\b', re.IGNORECASE),
                'confidence': 0.8
            },
            {
                'name': 'requires_external_knowledge',
                'regex': re.compile(r'\b(latest|current|recent|news|update|weather|stock|score|trend)\b', re.IGNORECASE),
                'confidence': 0.85
            },
            {
                'name': 'requires_tool_specific',
                'regex': None,  # Will check tool_name in prompt
                'confidence': 0.95
            }
        ]

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Analyze prompt to determine context requirements.
        Returns:
            Dictionary with detected patterns, entities, and confidence scores
        '''
        detected_patterns: List[Dict[str, Any]] = []
        entities: List[str] = []

        prompt_lower = prompt.lower()
        # Check each pattern
        for pattern in self.patterns:
            if pattern['name'] == 'requires_tool_specific':
                if tool_name and tool_name.lower() in prompt_lower:
                    detected_patterns.append({
                        'pattern': pattern['name'],
                        'confidence': pattern['confidence']
                    })
                    entities.append(tool_name)
            else:
                matches = pattern['regex'].findall(prompt)
                if matches:
                    detected_patterns.append({
                        'pattern': pattern['name'],
                        'confidence': pattern['confidence']
                    })
                    # Add matched entities (words/phrases)
                    if isinstance(matches[0], tuple):
                        for match in matches:
                            entities.extend([m for m in match if m])
                    else:
                        entities.extend(matches)

        # Remove duplicates and empty strings from entities
        entities = list({e.strip()
                        for e in entities if e and isinstance(e, str)})

        # Confidence score: average of detected patterns, or 0 if none
        if detected_patterns:
            confidence_score = sum(p['confidence']
                                   for p in detected_patterns) / len(detected_patterns)
        else:
            confidence_score = 0.0

        return {
            'detected_patterns': detected_patterns,
            'entities': entities,
            'confidence_score': round(confidence_score, 3)
        }
