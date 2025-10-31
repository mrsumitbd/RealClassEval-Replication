
import re
from typing import Any, Dict


class PromptPatternMatcher:
    """Analyzes prompts to determine context requirements."""

    def __init__(self):
        """Initialize pattern matchers."""
        # Define patterns for matching
        self.patterns = {
            'code_context': r'(code|snippet|function|method|class)',
            'error_context': r'(error|exception|stacktrace)',
            'conversation_context': r'(conversation|dialogue|chat)',
        }
        # Define entity extractors
        self.entity_extractors = {
            'code_entities': r'(`[^`]+`)',  # Extracts text within backticks
            # Extracts error/exception names
            'error_entities': r'([A-Za-z]+Error|[A-Za-z]+Exception)',
        }

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze prompt to determine context requirements.

        Returns:
            Dictionary with detected patterns, entities, and confidence scores
        """
        analysis_result = {'patterns': {}, 'entities': {}, 'confidence': {}}

        # Analyze patterns
        for pattern_name, pattern in self.patterns.items():
            if re.search(pattern, prompt, re.IGNORECASE):
                analysis_result['patterns'][pattern_name] = True
                # Confidence score for now is binary
                analysis_result['confidence'][pattern_name] = 1.0

        # Extract entities
        for entity_name, entity_extractor in self.entity_extractors.items():
            entities = re.findall(entity_extractor, prompt)
            if entities:
                analysis_result['entities'][entity_name] = entities

        return analysis_result
