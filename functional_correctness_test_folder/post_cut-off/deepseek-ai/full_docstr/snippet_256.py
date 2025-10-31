
from typing import Dict, Any


class PromptPatternMatcher:
    '''Analyzes prompts to determine context requirements.'''

    def __init__(self):
        '''Initialize pattern matchers.'''
        self.patterns = {
            "summarize": ["summarize", "brief", "overview"],
            "translate": ["translate", "convert to"],
            "generate": ["generate", "create", "write"],
            "classify": ["classify", "categorize", "label"]
        }

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Analyze prompt to determine context requirements.
        Returns:
            Dictionary with detected patterns, entities, and confidence scores
        '''
        detected_patterns = []
        confidence_scores = {}

        for pattern, keywords in self.patterns.items():
            for keyword in keywords:
                if keyword in prompt.lower():
                    detected_patterns.append(pattern)
                    confidence_scores[pattern] = confidence_scores.get(
                        pattern, 0) + 0.2

        entities = {}
        if "text" in arguments:
            entities["text"] = arguments["text"]

        result = {
            "detected_patterns": detected_patterns,
            "entities": entities,
            "confidence_scores": confidence_scores
        }

        return result
