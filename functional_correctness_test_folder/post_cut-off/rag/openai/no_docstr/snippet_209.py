
import pathlib
import re
from typing import Any, Dict, List, Optional, Tuple


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
        # Cache for compiled function patterns keyed by register name
        self._func_patterns: Dict[str, re.Pattern] = {}
        # Cache for function bodies keyed by function name
        self._func_bodies: Dict[str, str] = {}

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        """Get cached function pattern for register name."""
        if reg_name not in self._func_patterns:
            # Pattern matches a function definition that contains the register name
            # Handles multi-line function headers and bodies
            pattern = rf"""
                (?P<func_def>
                    (?:\b(?:module|task|function|always)\b.*?{re.escape(reg_name)}.*?;)?   # optional header
                    (?P<func_body>
                        \b(?:module|task|function|always)\b.*?{re.escape(reg_name)}.*?;.*?   # body start
                        (?:[^\{]*\{{[^\}]*\}}[^\{]*)*   # nested braces
                    )
                )
            """
            self._func_patterns[reg_name] = re.compile(
                pattern, re.DOTALL | re.VERBOSE)
        return self._func_patterns[reg_name]

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        """
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        """
        results: Dict[str, Any] = {}
        pattern = self._get_function_pattern(reg_name)
        for path, content in self.file_contents.items():
            for match in pattern.finditer(content):
                func_body = match.group('func_body')
                # Extract function name if possible
                func_name_match = re.search(
                    r'\b(?:module|task|function|always)\b\s+(\w+)', func_body)
                func_name = func_name_match.group(
                    1) if func_name_match else "<unknown>"
                timing = self._determine_timing(func_name, func_body)
                access = self._analyze_access_pattern(func_body, reg_name)
                results[path] = {
                    'function': func_name,
                    'body': func_body,
                    'timing': timing,
                    'access': access,
                }
        return results

    def _determine_timing(self, func_name: str, func_body: str) -> str:
        """
        Determine timing context with fallback detection.
        Args:
            func_name: Name of the function
            func_body: Content of the function
        Returns:
            Timing classification string
        """
        if re.search(r'@(posedge|negedge)', func_body):
            return 'edge'
        if re.search(r'@(\*|always)', func_body):
            return 'combinational'
        if re.search(r'#\s*\(', func_body) or re.search(r'#\s*\d+', func_body):
            return 'delay'
        return 'unknown'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        """Analyze register access patterns within a function."""
        read_pattern = re.compile(rf'\b{re.escape(reg_name)}\b(?!\s*=\s*)')
        write_pattern = re.compile(rf'\b{re.escape(reg_name)}\s*=\s*')
        reads = len(read_pattern.findall(func_body))
        writes = len(write_pattern.findall(func_body))
        if reads and writes:
            return 'read_write'
        if reads:
            return 'read'
        if writes:
            return 'write'
        return 'none'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Analyze register access sequences with improved function parsing.
        Enhanced to handle nested braces properly using balance counter.
        """
        sequences: List[Dict[str, Any]] = []
        for path, content in self.file_contents.items():
            # Find all function definitions
            func_pattern = re.compile(
                r'\b(?:module|task|function|always)\b\s+(\w+)\s*.*?;')
            for func_match in func_pattern.finditer(content):
                func_name = func_match.group(1)
                start = func_match.end()
                # Find matching closing brace using balance counter
                brace_balance = 0
                end = start
                while end < len(content):
                    if content[end] == '{':
                        brace_balance += 1
                    elif content[end] == '}':
                        if brace_balance == 0:
                            break
                        brace_balance -= 1
                    end += 1
                func_body = content[start:end]
                # If reg_name is None, analyze all registers
                if reg_name is None:
                    # Find all identifiers that look like registers
                    reg_candidates = set(re.findall(
                        r'\b([A-Za-z_]\w*)\b', func_body))
                else:
                    reg_candidates = {reg_name}
                accesses: List[Tuple[int, str]] = []
                for reg in reg_candidates:
                    # Find all occurrences with line numbers
                    for m in re.finditer(rf'\b{re.escape(reg)}\b', func_body):
                        line_no = func_body[:m.start()].count('\n') + 1
                        accesses.append((line_no, reg))
                if accesses:
                    sequences.append({
                        'file': str(path),
                        'function': func_name,
                        'accesses': accesses,
                    })
        return sequences

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Analyze timing constraints and delays related to register accesses."""
        constraints: List[Dict[str, Any]] = []
        delay_pattern = re.compile(r'#\s*\(?\s*(\d+\.?\d*)\s*\)?')
        for path, content in self.file_contents.items():
            for func_match in re.finditer(r'\b(?:module|task|function|always)\b\s+(\w+)\s*.*?;', content):
                func_name = func_match.group(1)
                start = func_match.end()
                brace_balance = 0
                end = start
                while end < len(content):
                    if content[end] == '{':
                        brace_balance += 1
                    elif content[end] == '}':
                        if brace_balance == 0:
                            break
                        brace_balance -= 1
                    end += 1
                func_body = content[start:end]
                for m in delay_pattern.finditer(func_body):
                    delay_val = m.group(1)
                    constraints.append({
                        'file': str(path),
                        'function': func_name,
                        'delay': float(delay_val),
                    })
        return constraints
