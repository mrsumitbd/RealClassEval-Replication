
import pathlib
import re
from typing import Any, Dict, List, Optional


class DriverAnalyzer:
    """
    Encapsulates driver analysis functionality with shared state.
    This class maintains pre-compiled regex patterns and file content
    to avoid duplication and improve performance.
    """

    def __init__(self, file_contents: Dict[pathlib.Path, str]):
        """
        Initialize analyzer with file contents.

        Args:
            file_contents: Dictionary mapping file paths to their content
        """
        self.file_contents = file_contents
        self.function_patterns = {}

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        """Get cached function pattern for register name."""
        if reg_name not in self.function_patterns:
            pattern = re.compile(
                rf'def\s+(\w+)\s*\([^)]*\)\s*:\s*.*{reg_name}.*', re.DOTALL | re.MULTILINE)
            self.function_patterns[reg_name] = pattern
        return self.function_patterns[reg_name]

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        """
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        """
        results = []
        pattern = self._get_function_pattern(reg_name)
        for file_path, content in self.file_contents.items():
            for match in pattern.finditer(content):
                func_name = match.group(1)
                func_body = self._extract_function_body(content, match.start())
                timing = self._determine_timing(func_name, func_body)
                results.append({
                    'file_path': file_path,
                    'function_name': func_name,
                    'timing': timing,
                    'register_access': self._analyze_access_pattern(func_body, reg_name)
                })
        return results

    def _extract_function_body(self, content: str, start_pos: int) -> str:
        """Extract function body from content starting at given position."""
        brace_count = 0
        body = ''
        for line in content[start_pos:].splitlines(True):
            body += line
            brace_count += line.count('{') - line.count('}')
            if brace_count == 0:
                break
        return body

    def _determine_timing(self, func_name: str, func_body: str) -> str:
        """
        Determine timing context with fallback detection.

        Args:
            func_name: Name of the function
            func_body: Content of the function

        Returns:
            Timing classification string
        """
        # Simple timing detection based on keyword presence
        if 'delay' in func_body.lower():
            return 'delayed'
        elif 'timeout' in func_body.lower():
            return 'timed_out'
        else:
            return 'unknown'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        """Analyze register access patterns within a function."""
        # Basic analysis: count read/write occurrences
        reads = func_body.count(reg_name)  # Simplification
        writes = func_body.count(f'{reg_name} =')  # Simplification
        return f'reads: {reads}, writes: {writes}'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Analyze register access sequences with improved function parsing.
        Enhanced to handle nested braces properly using balance counter.
        """
        results = []
        for file_path, content in self.file_contents.items():
            if reg_name:
                pattern = self._get_function_pattern(reg_name)
                for match in pattern.finditer(content):
                    func_name = match.group(1)
                    func_body = self._extract_function_body(
                        content, match.start())
                    results.append({
                        'file_path': file_path,
                        'function_name': func_name,
                        'register_access_sequence': self._analyze_access_pattern(func_body, reg_name)
                    })
            else:
                # If reg_name is None, analyze all functions
                for match in re.finditer(r'def\s+(\w+)\s*\([^)]*\)\s*:', content):
                    func_name = match.group(1)
                    func_body = self._extract_function_body(
                        content, match.start())
                    results.append({
                        'file_path': file_path,
                        'function_name': func_name,
                        'register_access_sequence': self._analyze_access_pattern(func_body, reg_name) if reg_name else 'N/A'
                    })
        return results

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Analyze timing constraints and delays related to register accesses."""
        results = []
        for file_path, content in self.file_contents.items():
            if reg_name:
                pattern = self._get_function_pattern(reg_name)
                for match in pattern.finditer(content):
                    func_name = match.group(1)
                    func_body = self._extract_function_body(
                        content, match.start())
                    timing = self._determine_timing(func_name, func_body)
                    results.append({
                        'file_path': file_path,
                        'function_name': func_name,
                        'timing_constraint': timing
                    })
            else:
                # If reg_name is None, analyze all functions for timing
                for match in re.finditer(r'def\s+(\w+)\s*\([^)]*\)\s*:', content):
                    func_name = match.group(1)
                    func_body = self._extract_function_body(
                        content, match.start())
                    timing = self._determine_timing(func_name, func_body)
                    results.append({
                        'file_path': file_path,
                        'function_name': func_name,
                        'timing_constraint': timing
                    })
        return results
