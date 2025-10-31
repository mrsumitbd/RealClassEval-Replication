
import re
from typing import Dict, Any


class PromptPatternMatcher:
    '''Analyzes prompts to determine context requirements.'''

    def __init__(self):
        '''Initialize pattern matchers.'''
        self.patterns = {
            'tool_usage': re.compile(r'\b(?:use|apply|utilize|employ)\s+the\s+(\w+)\s+tool\b', re.IGNORECASE),
            'entity_extraction': re.compile(r'\b(?:find|identify|locate|extract)\s+(?:the\s+)?([a-zA-Z\s]+)\b', re.IGNORECASE),
            'comparison': re.compile(r'\b(?:compare|contrast|difference|similarity)\s+between\b', re.IGNORECASE),
            'time_reference': re.compile(r'\b(?:last|previous|recent|past)\s+(\w+)\b', re.IGNORECASE),
            'quantitative': re.compile(r'\b(?:how\s+many|what\s+is\s+the\s+number|count|total)\b', re.IGNORECASE)
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

        # Check for tool usage patterns
        tool_match = self.patterns['tool_usage'].search(prompt)
        if tool_match and tool_match.group(1).lower() == tool_name.lower():
            results['patterns'].append('tool_usage')
            results['confidence'] += 0.3

        # Check for entity extraction patterns
        entity_match = self.patterns['entity_extraction'].search(prompt)
        if entity_match:
            results['patterns'].append('entity_extraction')
            results['entities'].append(entity_match.group(1).strip())
            results['confidence'] += 0.2

        # Check for comparison patterns
        if self.patterns['comparison'].search(prompt):
            results['patterns'].append('comparison')
            results['confidence'] += 0.2

        # Check for time reference patterns
        time_match = self.patterns['time_reference'].search(prompt)
        if time_match:
            results['patterns'].append('time_reference')
            results['entities'].append(time_match.group(1))
            results['confidence'] += 0.15

        # Check for quantitative patterns
        if self.patterns['quantitative'].search(prompt):
            results['patterns'].append('quantitative')
            results['confidence'] += 0.15

        # Adjust confidence based on number of detected patterns
        if len(results['patterns']) > 0:
            results['confidence'] = min(
                1.0, results['confidence'] * (1 + 0.1 * len(results['patterns'])))

        return results
