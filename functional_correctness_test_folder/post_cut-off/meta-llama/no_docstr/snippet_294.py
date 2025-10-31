
import re


class CodeManager:

    def __init__(self):
        self.raw_code = ""
        self.formatted_code = ""

    def update_from_response(self, response: str) -> None:
        self.raw_code = self._extract_code_with_fallbacks(response)
        self.formatted_code = self._extract_python_like_content(self.raw_code)

    def _extract_code_with_fallbacks(self, text: str) -> str:
        # Try to extract code block with triple backticks
        code_block_match = re.search(r'
