
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
            'conversation_context': r'(conversation|dialogue|chat)',
        }
        # Define entity extraction patterns
        self.entity_patterns = {
            'code_entities': r'(`[^`]+`)',  # matches code blocks
            # matches error names
            'error_entities': r'([A-Za-z]+Error|[A-Za-z]+Exception)',
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
                # confidence score for now is 1.0 if pattern is found
                results['confidence'][pattern_name] = 1.0
            else:
                results['patterns'][pattern_name] = False
                # confidence score for now is 0.0 if pattern is not found
                results['confidence'][pattern_name] = 0.0
        # Extract entities from prompt
        for entity_name, entity_pattern in self.entity_patterns.items():
            entities = re.findall(entity_pattern, prompt)
            results['entities'][entity_name] = entities
        return results
