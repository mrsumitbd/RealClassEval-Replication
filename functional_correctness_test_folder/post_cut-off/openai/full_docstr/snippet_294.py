
import re
from typing import List, Tuple


class CodeManager:
    '''
    Manages code content extraction, storage, and formatting.
    This class provides robust methods for extracting Python code from LLM responses
    using multiple fallback strategies, similar to HumanEval evaluator approaches.
    '''

    def __init__(self):
        '''Initialize code storage.'''
        self.codes: List[Tuple[str, str]] = []  # list of (filename, code)

    def update_from_response(self, response: str) -> None:
        '''
        Update codes from LLM response using robust extraction methods.
        Args:
            response: Raw LLM response text containing code
        '''
        extracted = self._extract_code_with_fallbacks(response)
        if extracted:
            # If multiple files are detected, they will be stored separately
            # otherwise store as main.py
            if isinstance(extracted, list):
                for filename, code in extracted:
                    self.codes.append((filename, code))
            else:
                self.codes.append(("main.py", extracted))

    def _extract_code_with_fallbacks(self, text: str) -> str | List[Tuple[str, str]]:
        '''
        Extract Python code from text using multiple fallback methods.
        This method tries several extraction strategies in order of preference:
        1. Look for "## Validated Code" section (from other agents)
        2. Extract from
