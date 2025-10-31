
import re


class CodeManager:

    def __init__(self):
        self._codes = []

    def update_from_response(self, response: str) -> None:
        code = self._extract_code_with_fallbacks(response)
        if code and code.strip():
            self._codes.append(code.strip())

    def _extract_code_with_fallbacks(self, text: str) -> str:
        # Try to extract code from triple backticks with python
        match = re.search(r"
