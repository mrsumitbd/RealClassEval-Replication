
from typing import Dict, Any, List
import re


class PromptPatternMatcher:
    """
    A simple prompt pattern matcher that replaces placeholders in a prompt
    with provided arguments and reports on the matching status.
    """

    def __init__(self):
        # Regex to find placeholders like {name}
        self.placeholder_pattern = re.compile(r'\{(\w+)\}')

    def analyze_prompt(self, prompt: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes the prompt for placeholders and the presence of the tool name.
        Replaces placeholders with corresponding argument values.

        Parameters
        ----------
        prompt : str
            The prompt string containing placeholders.
        tool_name : str
            The name of the tool to look for in the prompt.
        arguments : Dict[str, Any]
            A dictionary mapping placeholder names to their replacement values.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing:
                - original_prompt: The original prompt string.
                - processed_prompt: The prompt after placeholder replacement.
                - tool_name: The provided tool name.
                - arguments: The original arguments dictionary.
                - placeholders_found: List of placeholders found in the prompt.
                - placeholders_missing: List of placeholders that were not provided in arguments.
                - tool_name_present: Boolean indicating if the tool name appears in the prompt.
        """
        # Find all placeholders in the prompt
        placeholders: List[str] = self.placeholder_pattern.findall(prompt)

        # Determine missing placeholders
        placeholders_missing = [p for p in placeholders if p not in arguments]

        # Replace placeholders with provided arguments
        def replace(match: re.Match) -> str:
            key = match.group(1)
            return str(arguments.get(key, match.group(0)))

        processed_prompt = self.placeholder_pattern.sub(replace, prompt)

        # Check if tool name is present in the prompt
        tool_name_present = tool_name in prompt

        return {
            "original_prompt": prompt,
            "processed_prompt": processed_prompt,
            "tool_name": tool_name,
            "arguments": arguments,
            "placeholders_found": placeholders,
            "placeholders_missing": placeholders_missing,
            "tool_name_present": tool_name_present,
        }
