
class CodeManager:

    def __init__(self):
        self.raw_code = ""
        self.formatted_codes = ""

    def update_from_response(self, response: str) -> None:
        self.raw_code = self._extract_code_with_fallbacks(response)
        self.formatted_codes = self._extract_python_like_content(self.raw_code)

    def _extract_code_with_fallbacks(self, text: str) -> str:
        import re
        code_blocks = re.findall(r'
