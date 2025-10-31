
import re
from typing import Any, Dict


class PromptPatternMatcher:
    """Analyzes prompts to determine context requirements."""

    def __init__(self):
        """Initialize pattern matchers."""
        # Define regular expression patterns for matching
        self.patterns = {
            'code_context': r'(code|snippet|function|method|class)',
            'error_context': r'(error|exception|stacktrace)',
            'config_context': r'(config|configuration|settings)'
        }
        # Define entity extraction patterns
        self.entity_patterns = {
            'code_entities': r'([a-zA-Z_][a-zA-Z0-9_]*)',
            'error_entities': r'([A-Za-z]+Error|[A-Za-z]+Exception)'
        }

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze prompt to determine context requirements.

        Returns:
            Dictionary with detected patterns, entities, and confidence scores
        """
        results = {'patterns': {}, 'entities': {}, 'confidence': {}}

        # Analyze prompt for patterns
        for pattern_name, pattern in self.patterns.items():
            if re.search(pattern, prompt, re.IGNORECASE):
                results['patterns'][pattern_name] = True
                # Assign confidence score based on pattern match
                # default confidence score
                results['confidence'][pattern_name] = 0.8

        # Extract entities from prompt
        for entity_name, entity_pattern in self.entity_patterns.items():
            entities = re.findall(entity_pattern, prompt)
            if entities:
                results['entities'][entity_name] = entities

        # Adjust confidence scores based on entity extraction
        if results['entities']:
            for pattern_name in results['patterns']:
                if results['patterns'][pattern_name]:
                    # increase confidence score
                    results['confidence'][pattern_name] += 0.1

        # Ensure confidence scores are within valid range
        for pattern_name in results['confidence']:
            results['confidence'][pattern_name] = min(
                results['confidence'][pattern_name], 1.0)

        return results
