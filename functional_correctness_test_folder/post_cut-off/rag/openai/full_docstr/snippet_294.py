
import re
from typing import Dict, List


class CodeManager:
    """
    Manages code content extraction, storage, and formatting.
    This class provides robust methods for extracting Python code from LLM responses
    using multiple fallback strategies, similar to HumanEval evaluator approaches.
    """

    def __init__(self):
        """Initialize code storage."""
        self._codes: Dict[str, str] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def update_from_response(self, response: str) -> None:
        """
        Update codes from LLM response using robust extraction methods.
        Args:
            response: Raw LLM response text containing code
        """
        extracted = self._extract_code_with_fallbacks(response)
        if extracted:
            self._codes.update(self._parse_code_into_files(extracted))

    def get_formatted_codes(self) -> str:
        """
        Get formatted codes for display purposes.
        Returns:
            Formatted string with filename and code blocks
        """
        parts: List[str] = []
        for fname, code in sorted(self._codes.items()):
            parts.append(f"  # File: {fname}\n
