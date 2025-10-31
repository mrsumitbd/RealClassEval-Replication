import re
from typing import Dict, Any, List, Tuple, Optional

class CodeManager:
    """
    Manages code content extraction, storage, and formatting.

    This class provides robust methods for extracting Python code from LLM responses
    using multiple fallback strategies, similar to HumanEval evaluator approaches.
    """

    def __init__(self):
        """Initialize code storage."""
        self.codes: Dict[str, str] = {}
        self.default_filename = 'solution.py'

    def update_from_response(self, response: str) -> None:
        """
        Update codes from LLM response using robust extraction methods.

        Args:
            response: Raw LLM response text containing code
        """
        extracted_code = self._extract_code_with_fallbacks(response)
        if extracted_code:
            self.codes[self.default_filename] = extracted_code

    def _extract_code_with_fallbacks(self, text: str) -> str:
        """
        Extract Python code from text using multiple fallback methods.

        This method tries several extraction strategies in order of preference:
        1. Look for "## Validated Code" section (from other agents)
        2. Extract from ```python``` fenced blocks
        3. Find function definition patterns
        4. Parse filename + code patterns  
        5. Last resort: find any Python-like syntax

        Args:
            text: Input text containing code

        Returns:
            Extracted code string, or empty string if no code found
        """
        validated_match = re.search('##\\s*Validated Code\\s*```python\\s*([\\s\\S]*?)```', text, re.IGNORECASE)
        if validated_match:
            code = validated_match.group(1).strip()
            return code
        block_match = re.search('```python\\s*([\\s\\S]*?)```', text, re.IGNORECASE)
        if block_match:
            code = block_match.group(1).strip()
            return code
        function_match = re.search('(def\\s+\\w+\\s*\\(.*?\\):[\\s\\S]*?)(?=\\n{2,}|\\Z)', text)
        if function_match:
            code = function_match.group(1).strip()
            return code
        filename_pattern = '([a-z_]+\\.py)\\s*\\n\\s*```python\\s*(.*?)```'
        filename_matches = re.findall(filename_pattern, text, re.DOTALL)
        if filename_matches:
            code = filename_matches[0][1].strip()
            return code
        return self._extract_python_like_content(text)

    def _extract_python_like_content(self, text: str) -> str:
        """
        Last resort extraction method for Python-like content.

        Args:
            text: Input text

        Returns:
            Extracted Python-like code or empty string
        """
        lines = text.split('\n')
        code_lines = []
        in_function = False
        for line in lines:
            if 'def ' in line and '(' in line and (')' in line) and (':' in line):
                in_function = True
                code_lines.append(line)
            elif in_function:
                if line.strip() and (not line.startswith((' ', '\t'))) and ('def ' not in line):
                    break
                code_lines.append(line)
        return '\n'.join(code_lines) if code_lines else ''

    def get_formatted_codes(self) -> str:
        """
        Get formatted codes for display purposes.

        Returns:
            Formatted string with filename and code blocks
        """
        if not self.codes:
            return 'No codes available.'
        formatted_sections = []
        for filename, content in self.codes.items():
            formatted_sections.append(f'{filename}:\n```python\n{content}\n```')
        return '\n\n'.join(formatted_sections)

    def get_raw_code(self) -> str:
        """
        Get raw code content without formatting.

        Returns:
            Raw code string, concatenated if multiple files exist
        """
        if not self.codes:
            return ''
        if len(self.codes) == 1:
            return list(self.codes.values())[0]
        return '\n\n'.join(self.codes.values())

    def has_code(self) -> bool:
        """Check if any code has been stored."""
        return bool(self.codes and any((code.strip() for code in self.codes.values())))