
from typing import Dict, Any


class PromptPatternMatcher:

    def __init__(self):
        self.patterns = {
            "tool1": r"^tool1\s+([a-zA-Z0-9]+)\s+([a-zA-Z0-9]+)$",
            "tool2": r"^tool2\s+([a-zA-Z0-9]+)$"
        }
        import re
        self.re = re

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name not in self.patterns:
            return {"error": f"Unsupported tool: {tool_name}"}

        pattern = self.patterns[tool_name]
        match = self.re.match(pattern, prompt)

        if match is None:
            return {"error": f"Prompt does not match the expected pattern for {tool_name}"}

        groups = match.groups()
        if tool_name == "tool1":
            if len(groups) != 2:
                return {"error": f"Invalid number of arguments for {tool_name}"}
            arguments["arg1"] = groups[0]
            arguments["arg2"] = groups[1]
        elif tool_name == "tool2":
            if len(groups) != 1:
                return {"error": f"Invalid number of arguments for {tool_name}"}
            arguments["arg"] = groups[0]

        return {"success": True, "arguments": arguments}
