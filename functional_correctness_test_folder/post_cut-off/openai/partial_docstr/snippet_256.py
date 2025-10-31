
import re
from typing import Dict, Any, List


class PromptPatternMatcher:
    '''Analyzes prompts to determine context requirements.'''

    def __init__(self):
        # Precompile a regex that detects words indicating a need for context
        self.context_regex = re.compile(
            r'\b(context|background|history|previous|past)\b', re.I
        )

    def analyze_prompt(
        self,
        prompt: str,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze the given prompt to determine:
        - Whether the prompt indicates a need for context.
        - Whether the specified tool is referenced.
        - Which argument keys are mentioned in the prompt.

        Parameters
        ----------
        prompt : str
            The user prompt to analyze.
        tool_name : str
            The name of the tool to look for in the prompt.
        arguments : Dict[str, Any]
            A dictionary of argument names that may appear in the prompt.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing analysis results.
        """
        # Detect context requirement
        requires_context = bool(self.context_regex.search(prompt))

        # Detect tool usage
        tool_regex = re.compile(r'\b' + re.escape(tool_name) + r'\b', re.I)
        tool_used = bool(tool_regex.search(prompt))

        # Detect argument mentions
        arguments_present: List[str] = []
        for key in arguments:
            # Use word boundaries to avoid partial matches
            key_regex = re.compile(r'\b' + re.escape(key) + r'\b', re.I)
            if key_regex.search(prompt):
                arguments_present.append(key)

        # Build result dictionary
        result: Dict[str, Any] = {
            'requires_context': requires_context,
            'tool_used': tool_used,
            'arguments_present': arguments_present,
            'prompt_length': len(prompt),
            'matched_tool_name': tool_name if tool_used else None,
        }

        return result
