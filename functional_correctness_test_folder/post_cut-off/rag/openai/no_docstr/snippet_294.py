
import re
from typing import Dict, List


class CodeManager:
    """
    Manages code content extraction, storage, and formatting.
    This class provides robust methods for extracting Python code from LLM responses
    using multiple fallback strategies, similar to HumanEval evaluator approaches.
    """

    def __init__(self):
        """Initialize code storage."""
        # Store code as a mapping from filename to code string
        self._codes: Dict[str, str] = {}

    def update_from_response(self, response: str) -> None:
        """
        Update codes from LLM response using robust extraction methods.
        Args:
            response: Raw LLM response text containing code
        """
        extracted = self._extract_code_with_fallbacks(response)
        if not extracted:
            return

        # Split into potential multiple files by "## filename:" markers
        parts = re.split(r'(?m)^##\s*filename:\s*(.+)$', extracted)
        # parts will be like ['', 'file1.py', 'code1', 'file2.py', 'code2', ...]
        # The first element is before the first marker (may contain code without filename)
        if parts[0].strip():
            # No filename marker at start, treat as main.py
            self._codes["main.py"] = parts[0].strip()

        # Process subsequent pairs
        for i in range(1, len(parts) - 1, 2):
            filename = parts[i].strip()
            code_block = parts[i + 1].strip()
            # If code_block contains fenced block, extract inside
            fenced = re.search(r'
