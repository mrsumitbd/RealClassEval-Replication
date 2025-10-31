
import pathlib
import re
from typing import Any, Dict, List, Optional, Tuple


class DriverAnalyzer:
    """
    Encapsulates driver analysis functionality with shared state.
    This class maintains pre-compiled regex patterns and file content
    to avoid duplication and improve performance.
    """

    # Regex flags used for all patterns
    _RE_FLAGS = re.IGNORECASE | re.MULTILINE | re.DOTALL

    def __init__(self, file_contents: Dict[pathlib.Path, str]):
        """
        Initialize analyzer with file contents.
        Args:
            file_contents: Dictionary mapping file paths to their content
        """
        self.file_contents = file_contents
        # Cache of compiled function header patterns per register name
        self._func_patterns: Dict[str, re.Pattern] = {}
        # Cache of extracted functions per file to avoid re‑parsing
        self._functions_cache: Dict[pathlib.Path, List[Tuple[str, str]]] = {}

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------
    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        """
        Get cached function pattern for register name.
        The pattern matches a function header; the body is extracted
        separately using a brace counter.
        """
        if reg_name not in self._func_patterns:
            # Basic C function header pattern (void, int, char, etc.)
            header_pat = (
                r'\b(?:static\s+)?(?:inline\s+)?(?:void|int|char|float|double|bool)'
                r'\s+(\w+)\s*\([^)]*\)\s*\{'
            )
            self._func_patterns[reg_name] = re.compile(
                header_pat, self._RE_FLAGS)
        return self._func_patterns[reg_name]

    def _extract_functions(self, content: str) -> List[Tuple[str, str]]:
        """
        Extract all function definitions from a file content.
        Returns a list of (function_name, function_body) tuples.
        """
        header_pat = (
            r'\b(?:static\s+)?(?:inline\s+)?(?:void|int|char|float|double|bool)'
            r'\s+(\w+)\s*\([^)]*\)\s*\{'
        )
        header_re = re.compile(header_pat, self._RE_FLAGS)
        functions: List[Tuple[str, str]] = []

        for match in header_re.finditer(content):
            func_name = match.group(1)
            body_start = match.end()  # position after the opening brace
            brace_count = 1
            pos = body_start
            while pos < len(content) and brace_count > 0:
                if content[pos] == '{':
                    brace_count += 1
                elif content[pos] == '}':
                    brace_count -= 1
                pos += 1
            body
