
import re
from typing import Dict


class CodeManager:
    '''
    Manages code content extraction, storage, and formatting.
    This class provides robust methods for extracting Python code from LLM responses
    using multiple fallback strategies, similar to HumanEval evaluator approaches.
    '''

    def __init__(self):
        '''Initialize code storage.'''
        self.codes: Dict[str, str] = {}  # filename -> code

    def update_from_response(self, response: str) -> None:
        '''
        Update codes from LLM response using robust extraction methods.
        Args:
            response: Raw LLM response text containing code
        '''
        code_map = self._extract_code_with_fallbacks(response)
        if isinstance(code_map, dict):
            self.codes = code_map
        elif isinstance(code_map, str):
            self.codes = {"main.py": code_map}
        else:
            self.codes = {}

    def _extract_code_with_fallbacks(self, text: str):
        '''
        Extract Python code from text using multiple fallback methods.
        This method tries several extraction strategies in order of preference:
        1. Look for "## Validated Code" section (from other agents)
        2. Extract from
