
from typing import Dict, Any, Optional
import re


class PromptPatternMatcher:

    def __init__(self):
        self.patterns = {}

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name not in self.patterns:
            self._create_pattern(tool_name, arguments)

        pattern = self.patterns[tool_name]
        match = re.search(pattern, prompt)
        if match:
            return match.groupdict()
        return {}

    def _create_pattern(self, tool_name: str, arguments: Dict[str, Any]):
        pattern = rf"{tool_name}\("
        arg_patterns = []
        for arg_name, arg_type in arguments.items():
            if arg_type == str:
                arg_patterns.append rf"{arg_name}: (?P<{arg_name}>[^\s,]+)")
            elif arg_type == int:
                arg_patterns.append rf"{arg_name}: (?P<{arg_name}>-?\d+)")
            elif arg_type == float:
                arg_patterns.append rf"{arg_name}: (?P<{arg_name}>-?\d+\.\d+)")
            # Add more types as necessary
        pattern += ", ".join(arg_patterns) + r"\)"
        self.patterns[tool_name] = pattern
