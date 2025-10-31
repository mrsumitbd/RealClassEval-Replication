
import re
from typing import Any, Dict, List


class PromptPatternMatcher:
    '''Analyzes prompts to determine context requirements.'''

    def __init__(self):
        '''Initialize pattern matchers.'''
        # Patterns that indicate a tool invocation or context requirement
        self._patterns: List[re.Pattern] = [
            re.compile(r'\b(use|invoke|call|execute)\b', re.IGNORECASE),
            re.compile(r'\b(tool|assistant|function)\b', re.IGNORECASE),
            re.compile(r'\b(argument|parameter|input)\b', re.IGNORECASE),
            re.compile(r'\b(please|kindly|could you)\b', re.IGNORECASE),
            re.compile(r'\b(help|assist|support)\b', re.IGNORECASE),
        ]

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Analyze prompt to determine context requirements.
        Returns:
            Dictionary with detected patterns, entities, and confidence scores
        '''
        matched_patterns: List[str] = []

        # Find all pattern matches in the prompt
        for pat in self._patterns:
            if pat.search(prompt):
                matched_patterns.append(pat.pattern)

        # Basic confidence: proportion of patterns matched out of total patterns
        confidence = len(matched_patterns) / \
            len(self._patterns) if self._patterns else 0.0

        # Build result dictionary
        result: Dict[str, Any] = {
            'patterns': matched_patterns,
            'entities': {
                'tool_name': tool_name,
                'arguments': arguments,
            },
            'confidence': round(confidence, 3),
        }

        return result
