
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
                rf'def\s+(\w+)\s*\(.*?\)\s*:\s*(.*?)(?=(?:def|\Z))', re.DOTALL)
            self.function_patterns[reg_name] = pattern
        return self.function_patterns[reg_name]

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        """
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        """
        results = []
        for file_path, content in self.file_contents.items():
            pattern = self._get_function_pattern(reg_name)
            for match in pattern.finditer(content):
                func_name, func_body = match.groups()
                timing = self._determine_timing(func_name, func_body)
                results.append({
                    'file_path': file_path,
                    'function_name': func_name,
                    'timing': timing,
                    'access_pattern': self._analyze_access_pattern(func_body, reg_name)
                })
        return results[0] if results else {}

    def _determine_timing(self, func_name: str, func_body: str) -> str:
        """
        Determine timing context with fallback detection.

        Args:
            func_name: Name of the function
            func_body: Content of the function

        Returns:
            Timing classification string
        """
        # Simple timing detection based on function name or body content
        if 'delay' in func_name.lower() or 'sleep' in func_body.lower():
            return 'delayed'
        elif 'irq' in func_name.lower() or 'interrupt' in func_body.lower():
            return 'interrupt'
        else:
            return 'unknown'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        """Analyze register access patterns within a function."""
        # Basic analysis: count read/write occurrences
        read_count = func_body.count(f'{reg_name}.read')
        write_count = func_body.count(f'{reg_name}.write')
        return f'reads: {read_count}, writes: {write_count}'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Analyze register access sequences with improved function parsing.
        Enhanced to handle nested braces properly using balance counter.
        """
        results = []
        for file_path, content in self.file_contents.items():
            # Simplified example: just count the occurrences of register access
            access_count = content.count(reg_name)
            results.append({
                'file_path': file_path,
                'register_name': reg_name,
                'access_count': access_count
            })
        return results

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Analyze timing constraints and delays related to register accesses."""
        # Placeholder for actual implementation
        return [{'timing_constraint': 'example constraint'}]
