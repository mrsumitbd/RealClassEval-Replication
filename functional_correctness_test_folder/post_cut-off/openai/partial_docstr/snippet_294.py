
import re
from typing import List


class CodeManager:
    '''
    Manages code content extraction, storage, and formatting.
    This class provides robust methods for extracting Python code from LLM responses
    using multiple fallback strategies, similar to HumanEval evaluator approaches.
    '''

    def __init__(self):
        # Store extracted code snippets
        self._codes: List[str] = []

    def update_from_response(self, response: str) -> None:
        """
        Extract code from the given response and store it.
        """
        code = self._extract_code_with_fallbacks(response)
        if code:
            # Normalize line endings and strip surrounding whitespace
            cleaned = "\n".join(line.rstrip()
                                for line in code.splitlines()).strip()
            if cleaned:
                self._codes.append(cleaned)

    def _extract_code_with_fallbacks(self, text: str) -> str:
        """
        Extract Python code from text using multiple fallback methods.
        This method tries several extraction strategies in order of preference:
        1. Look for "## Validated Code" section (from other agents)
        2. Extract from
