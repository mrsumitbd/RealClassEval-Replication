
import re


class CodeManager:
    '''
    Manages code content extraction, storage, and formatting.
    This class provides robust methods for extracting Python code from LLM responses
    using multiple fallback strategies, similar to HumanEval evaluator approaches.
    '''

    def __init__(self):
        '''Initialize code storage.'''
        self.codes = {}

    def update_from_response(self, response: str) -> None:
        '''
        Update codes from LLM response using robust extraction methods.
        Args:
            response: Raw LLM response text containing code
        '''
        code = self._extract_code_with_fallbacks(response)
        if code:
            self.codes['extracted_code.py'] = code.strip()

    def _extract_code_with_fallbacks(self, text: str) -> str:
        '''
        Extract Python code from text using multiple fallback methods.
        This method tries several extraction strategies in order of preference:
        1. Look for "## Validated Code" section (from other agents)
        2. Extract from
