
import re


class CodeManager:
    '''
    Manages code content extraction, storage, and formatting.
    This class provides robust methods for extracting Python code from LLM responses
    using multiple fallback strategies, similar to HumanEval evaluator approaches.
    '''

    def __init__(self):
        self._raw_code = ""

    def update_from_response(self, response: str) -> None:
        code = self._extract_code_with_fallbacks(response)
        self._raw_code = code.strip() if code else ""

    def _extract_code_with_fallbacks(self, text: str) -> str:
        # 1. Look for "## Validated Code" section
        validated_code_match = re.search(
            r"##\s*Validated Code\s*\n+((?:.|\n)+?)(?:\n##|$)", text, re.IGNORECASE)
        if validated_code_match:
            code = validated_code_match.group(1)
            code = self._extract_python_like_content(code)
            if code:
                return code

        # 2. Extract from
