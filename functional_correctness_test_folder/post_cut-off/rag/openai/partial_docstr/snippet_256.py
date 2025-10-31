
import re
from typing import Any, Dict, List


class PromptPatternMatcher:
    """Analyzes prompts to determine context requirements."""

    def __init__(self):
        """Initialize pattern matchers."""
        # Define a set of common intent patterns with corresponding regexes.
        self._patterns: Dict[str, re.Pattern] = {
            "list": re.compile(r"\b(?:list|show|display|enumerate)\b", re.IGNORECASE),
            "summary": re.compile(r"\b(?:summary|summarize|overview|brief)\b", re.IGNORECASE),
            "calculate": re.compile(r"\b(?:calculate|compute|find|determine|evaluate)\b", re.IGNORECASE),
            "search": re.compile(r"\b(?:search|find|lookup|locate|retrieve)\b", re.IGNORECASE),
            "filter": re.compile(r"\b(?:filter|exclude|remove|discard)\b", re.IGNORECASE),
            "sort": re.compile(r"\b(?:sort|order|arrange|rank)\b", re.IGNORECASE),
            "delete": re.compile(r"\b(?:delete|remove|erase|discard)\b", re.IGNORECASE),
            "update": re.compile(r"\b(?:update|modify|change|edit)\b", re.IGNORECASE),
            "create": re.compile(r"\b(?:create|add|insert|generate)\b", re.IGNORECASE),
            "help": re.compile(r"\b(?:help|assist|guide|support)\b", re.IGNORECASE),
        }

    def analyze_prompt(
        self, prompt: str, tool_name: str, arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze prompt to determine context requirements.

        Parameters
        ----------
        prompt : str
            The user prompt to analyze.
        tool_name : str
            Name of the tool being invoked.
        arguments : Dict[str, Any]
            Arguments supplied to the tool.

        Returns
        -------
        Dict[str, Any]
            Dictionary with detected patterns, entities, and confidence scores.
        """
        if not isinstance(prompt, str):
            raise TypeError("prompt must be a string")

        # Normalize prompt for matching
        prompt_lower = prompt.lower()

        matched_patterns: List[str] = []
        matched_phrases: Dict[str, List[str]] = {}

        for name, regex in self._patterns.items():
            matches = regex.findall(prompt_lower)
            if matches:
                matched_patterns.append(name)
                matched_phrases[name] = matches

        # Confidence calculation: base 0.5 + 0.5 * (matches / total patterns)
        total_patterns = len(self._patterns)
        confidence = 0.5
        if total_patterns > 0:
            confidence += 0.5 * (len(matched_patterns) / total_patterns)

        # Clamp confidence to [0, 1]
        confidence = max(0.0, min(1.0, confidence))

        result: Dict[str, Any] = {
            "patterns": matched_patterns,
            "matched_phrases": matched_phrases,
            "entities": {
                "tool": tool_name,
                "arguments": arguments,
            },
            "confidence": confidence,
        }

        return result
