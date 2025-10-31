
from typing import Dict, Any


class PromptPatternMatcher:
    '''Analyzes prompts to determine context requirements.'''

    def __init__(self):
        pass

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        analysis_result = {
            "prompt": prompt,
            "tool_name": tool_name,
            "arguments": arguments,
            "context_requirements": {
                "requires_external_knowledge": False,
                "requires_user_context": False,
                "requires_tool_specific_context": False
            }
        }

        if "research" in prompt.lower() or "look up" in prompt.lower():
            analysis_result["context_requirements"]["requires_external_knowledge"] = True

        if "you" in prompt.lower() or "your" in prompt.lower():
            analysis_result["context_requirements"]["requires_user_context"] = True

        if tool_name in ["calculator", "calendar"]:
            analysis_result["context_requirements"]["requires_tool_specific_context"] = True

        return analysis_result
