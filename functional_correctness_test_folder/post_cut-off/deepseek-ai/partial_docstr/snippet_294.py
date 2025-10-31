
import re


class CodeManager:
    '''
    Manages code content extraction, storage, and formatting.
    This class provides robust methods for extracting Python code from LLM responses
    using multiple fallback strategies, similar to HumanEval evaluator approaches.
    '''

    def __init__(self):
        self._raw_code = ""
        self._formatted_code = ""

    def update_from_response(self, response: str) -> None:
        self._raw_code = self._extract_code_with_fallbacks(response)
        self._formatted_code = self._raw_code  # Can be extended for formatting

    def _extract_code_with_fallbacks(self, text: str) -> str:
        '''
        Extract Python code from text using multiple fallback methods.
        This method tries several extraction strategies in order of preference:
        1. Look for "## Validated Code" section (from other agents)
        2. Extract from
