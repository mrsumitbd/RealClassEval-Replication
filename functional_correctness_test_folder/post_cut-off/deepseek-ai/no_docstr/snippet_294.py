
class CodeManager:

    def __init__(self):
        self._raw_code = ""
        self._formatted_codes = ""

    def update_from_response(self, response: str) -> None:
        self._raw_code = self._extract_code_with_fallbacks(response)
        self._formatted_codes = self._raw_code

    def _extract_code_with_fallbacks(self, text: str) -> str:
        extracted_code = self._extract_python_like_content(text)
        if not extracted_code:
            extracted_code = text
        return extracted_code

    def _extract_python_like_content(self, text: str) -> str:
        lines = text.split('\n')
        code_lines = []
        in_code_block = False

        for line in lines:
            if line.strip().startswith('
