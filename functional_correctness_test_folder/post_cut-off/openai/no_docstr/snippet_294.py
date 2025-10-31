
import re
from typing import List


class CodeManager:
    def __init__(self):
        # Store extracted code blocks as a list of strings
        self._code_blocks: List[str] = []

    def update_from_response(self, response: str) -> None:
        """
        Extract code from the given response string and store it.
        """
        extracted = self._extract_code_with_fallbacks(response)
        if extracted:
            # Split into individual blocks if multiple fences were found
            blocks = [block.strip()
                      for block in extracted.split("\n\n") if block.strip()]
            self._code_blocks.extend(blocks)

    def _extract_code_with_fallbacks(self, text: str) -> str:
        """
        Try to extract code using markdown fences first.
        If none found, fall back to extracting python-like content.
        """
        # Pattern for
