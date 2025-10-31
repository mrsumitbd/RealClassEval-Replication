
import re
from typing import List


class CodeManager:
    '''
    Manages code content extraction, storage, and formatting.
    This class provides robust methods for extracting Python code from LLM responses
    using multiple fallback strategies, similar to HumanEval evaluator approaches.
    '''

    def __init__(self):
        self._codes: List[str] = []
        self._latest: str = ""

    def update_from_response(self, response: str) -> None:
        if not isinstance(response, str) or not response.strip():
            return
        code = self._extract_code_with_fallbacks(response)
        self._latest = code
        if code:
            self._codes.append(code)

    def _extract_code_with_fallbacks(self, text: str) -> str:
        '''
        Extract Python code from text using multiple fallback methods.
        This method tries several extraction strategies in order of preference:
        1. Look for "## Validated Code" section (from other agents)
        2. Extract from
