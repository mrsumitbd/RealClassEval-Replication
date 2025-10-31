
from typing import Dict, Any
import re


class PromptPatternMatcher:
    '''Analyzes prompts to determine context requirements.'''

    def __init__(self):
        self.context_keywords = [
            'context', 'previous', 'history', 'above', 'before', 'earlier', 'prior', 'conversation', 'chat'
        ]
        self.patterns = [
            re.compile(
                r'\b(use|with|based on|consider|given|according to|from)\b.*\b(context|history|conversation|chat)\b', re.IGNORECASE),
            re.compile(
                r'\b(context|history|conversation|chat)\b.*\b(required|needed|necessary|relevant|important)\b', re.IGNORECASE),
            re.compile(
                r'\b(previous|prior|earlier|above|before)\b.*\b(message|prompt|conversation|chat|context)\b', re.IGNORECASE),
        ]

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        result = {
            'requires_context': False,
            'context_type': None,
            'matched_keywords': [],
            'matched_patterns': []
        }
        prompt_lower = prompt.lower()
        matched_keywords = [
            kw for kw in self.context_keywords if kw in prompt_lower]
        matched_patterns = [
            pat.pattern for pat in self.patterns if pat.search(prompt)]
        if matched_keywords or matched_patterns:
            result['requires_context'] = True
            result['matched_keywords'] = matched_keywords
            result['matched_patterns'] = matched_patterns
            # Guess context type
            if any(word in prompt_lower for word in ['history', 'conversation', 'chat']):
                result['context_type'] = 'conversation_history'
            elif any(word in prompt_lower for word in ['previous', 'prior', 'earlier', 'above', 'before']):
                result['context_type'] = 'previous_message'
            else:
                result['context_type'] = 'general_context'
        return result
