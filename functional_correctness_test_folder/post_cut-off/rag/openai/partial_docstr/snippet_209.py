
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
        self._pattern_cache: Dict[str, re.Pattern] = {}

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        """
        Get cached function pattern for register name.
        """
        if reg_name not in self._pattern_cache:
            # Pattern matches a C function definition that contains the register name
            pattern = (
                r'(?P<func>void\s+(?P<name>\w+)\s*\([^)]*\)\s*\{'
                r'(?P<body>.*?)\})'
            )
            # Ensure the body contains the register name
            full_pattern = (
                r'(?P<func>void\s+(?P<name>\w+)\s*\([^)]*\)\s*\{'
                r'(?P<body>.*?'
                r'\b' + re.escape(reg_name) + r'\b.*?'
                r')\})'
            )
            compiled = re.compile(full_pattern, re.DOTALL | re.MULTILINE)
            self._pattern_cache[reg_name] = compiled
        return self._pattern_cache[reg_name]

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        """
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        """
        pattern = self._get_function_pattern(reg_name)
        for file_path, content in self.file_contents.items():
            for match in pattern.finditer(content):
                func_name = match.group('name')
                body = match.group('body')
                timing = self._determine_timing(func_name, body)
                access_pattern = self._analyze_access_pattern(body, reg_name)
                return {
                    'file': file_path,
                    'function_name': func_name,
                    'body': body,
                    'timing': timing,
                    'access_pattern': access_pattern,
                }
        return {}

    def _determine_timing(self, func_name: str, func_body: str) -> str:
        """
        Determine timing context with fallback detection.
        Args:
            func_name: Name of the function
            func_body: Content of the function
        Returns:
            Timing classification string
        """
        name_lower = func_name.lower()
        if any(keyword in name_lower for keyword in ('init', 'setup', 'reset', 'config')):
            return 'initialization'
        if any(keyword in name_lower for keyword in ('read', 'write', 'update', 'access')):
            return 'operational'
        # Fallback: look for delay calls
        if re.search(r'delay_(ms|us|ns)\s*\(', func_body):
            return 'delayed'
        return 'unknown'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        """
        Analyze register access patterns within a function.
        """
        read = bool(re.search(rf'\b{re.escape(reg_name)}\b', func_body))
        write = bool(re.search(rf'{re.escape(reg_name)}\s*=\s*', func_body))
        read_write = read and write
        if read_write:
            return 'read_write'
        if write:
            return 'write'
        if read:
            return 'read'
        return 'none'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Analyze register access sequences with improved function parsing.
        Enhanced to handle nested braces properly using balance counter.
        """
        results: List[Dict[str, Any]] = []
        # Regex to find function definitions (simple heuristic)
        func_def_re = re.compile(
            r'void\s+(\w+)\s*\([^)]*\)\s*\{', re.MULTILINE)
        for file_path, content in self.file_contents.items():
            pos = 0
            while True:
                match = func_def_re.search(content, pos)
                if not match:
                    break
                func_name = match.group(1)
                start = match.end()
                # Find matching closing brace using balance counter
                brace_count = 1
                i = start
                while i < len(content) and brace_count:
                    if content[i] == '{':
                        brace_count += 1
                    elif content[i] == '}':
                        brace_count -= 1
                    i += 1
                body = content[start:i-1]
                # Determine if this function contains the register(s)
                if reg_name:
                    if reg_name not in body:
                        pos = i
                        continue
                    accesses = self._analyze_access_pattern(body, reg_name)
                    timing = self._determine_timing(func_name, body)
                    results.append({
                        'file': file_path,
                        'function_name': func_name,
                        'body': body,
                        'access_pattern': accesses,
                        'timing': timing,
                    })
                else:
                    # Find all register names in body (simple pattern)
                    regs = set(re.findall(r'\b([A-Z0-9_]+_REG)\b', body))
                    for r in regs:
                        accesses = self._analyze_access_pattern(body, r)
                        timing = self._determine_timing(func_name, body)
                        results.append({
                            'file': file_path,
                            'function_name': func_name,
                            'body': body,
                            'register': r,
                            'access_pattern': accesses,
                            'timing': timing,
                        })
                pos = i
        return results

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Analyze timing constraints and delays related to register accesses.
        """
        delay_re = re
