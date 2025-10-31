
import re
from typing import Dict, Any


class PromptPatternMatcher:
    '''Analyzes prompts to determine context requirements.'''

    def __init__(self):
        '''Initialize pattern matchers.'''
        self.patterns = {
            'greeting': re.compile(r'\b(hi|hello|hey)\b', re.IGNORECASE),
            'question': re.compile(r'\?', re.IGNORECASE),
            'statement': re.compile(r'\.', re.IGNORECASE),
        }
        self.entities = {
            'name': re.compile(r'\b(my name is|i am)\s+(\w+)', re.IGNORECASE),
        }

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Analyze prompt to determine context requirements.
        Returns:
            Dictionary with detected patterns, entities, and confidence scores
        '''
        result = {'patterns': {}, 'entities': {}, 'confidence': {}}

        for pattern_name, pattern in self.patterns.items():
            if pattern.search(prompt):
                result['patterns'][pattern_name] = True
                # confidence score for pattern match
                result['confidence'][pattern_name] = 1.0

        for entity_name, entity_pattern in self.entities.items():
            match = entity_pattern.search(prompt)
            if match:
                result['entities'][entity_name] = match.group(
                    2)  # extract the entity value
                # confidence score for entity extraction
                result['confidence'][entity_name] = 1.0

        return result


# Example usage:
if __name__ == "__main__":
    matcher = PromptPatternMatcher()
    prompt = "Hello, my name is John. How are you?"
    tool_name = "example_tool"
    arguments = {}
    result = matcher.analyze_prompt(prompt, tool_name, arguments)
    print(result)
