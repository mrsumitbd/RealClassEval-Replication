
import re
from typing import Any, Dict, List


class PromptPatternMatcher:
    '''Analyzes prompts to determine context requirements.'''

    def __init__(self):
        '''Initialize pattern matchers.'''
        # Define a set of common action patterns
        self._patterns: Dict[str, re.Pattern] = {
            'list': re.compile(r'\b(list|show|display|enumerate)\b', re.IGNORECASE),
            'summary': re.compile(r'\b(summary|summarize|overview|brief)\b', re.IGNORECASE),
            'calculate': re.compile(r'\b(calculate|compute|find|determine|evaluate)\b', re.IGNORECASE),
            'convert': re.compile(r'\b(convert|translate|transform|change)\b', re.IGNORECASE),
            'search': re.compile(r'\b(search|find|lookup|locate|discover)\b', re.IGNORECASE),
            'generate': re.compile(r'\b(generate|create|build|produce|compose)\b', re.IGNORECASE),
            'delete': re.compile(r'\b(delete|remove|drop|erase|discard)\b', re.IGNORECASE),
            'update': re.compile(r'\b(update|modify|change|edit|revise)\b', re.IGNORECASE),
            'install': re.compile(r'\b(install|setup|configure|enable|activate)\b', re.IGNORECASE),
        }

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Analyze prompt to determine context requirements.
        Returns:
            Dictionary with detected patterns, entities, and confidence scores
        '''
        prompt_lower = prompt.lower()
        detected_patterns: List[str] = []

        # Detect patterns
        for name, regex in self._patterns.items():
            if regex.search(prompt):
                detected_patterns.append(name)

        # Detect entities
        entities: Dict[str, Any] = {}
        # Tool name presence
        entities['tool_name_present'] = tool_name.lower() in prompt_lower

        # Argument names presence
        arg_matches: List[str] = []
        for arg in arguments:
            if arg.lower() in prompt_lower:
                arg_matches.append(arg)
        entities['arguments_present'] = arg_matches

        # Confidence calculation
        # Base confidence on number of matched patterns relative to total patterns
        pattern_confidence = len(detected_patterns) / \
            len(self._patterns) if self._patterns else 0.0
        # Adjust confidence if tool name or arguments are mentioned
        entity_bonus = 0.0
        if entities['tool_name_present']:
            entity_bonus += 0.1
        if entities['arguments_present']:
            entity_bonus += 0.1 * len(entities['arguments_present'])
        confidence = min(pattern_confidence + entity_bonus, 1.0)

        return {
            'patterns': detected_patterns,
            'entities': entities,
            'confidence': round(confidence, 3),
        }
