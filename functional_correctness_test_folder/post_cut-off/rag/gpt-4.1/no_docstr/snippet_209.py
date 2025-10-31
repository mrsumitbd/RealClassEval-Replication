import re
import pathlib
from typing import Dict, Any, Optional, List


class DriverAnalyzer:
    '''
    Encapsulates driver analysis functionality with shared state.
    This class maintains pre-compiled regex patterns and file content
    to avoid duplication and improve performance.
    '''

    def __init__(self, file_contents: Dict[pathlib.Path, str]):
        '''
        Initialize analyzer with file contents.
        Args:
            file_contents: Dictionary mapping file paths to their content
        '''
        self.file_contents = file_contents
        self._function_patterns: Dict[str, re.Pattern] = {}

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        '''Get cached function pattern for register name.'''
        if reg_name not in self._function_patterns:
            # Function pattern: matches C-style function definitions containing reg_name
            # Handles macros split across lines (with backslash)
            pattern = (
                # return type and function name
                r'([a-zA-Z_][a-zA-Z0-9_*\s]+)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*'
                # arguments
                r'\(([^)]*)\)\s*'
                # opening brace
                r'\{'
                # function body (non-greedy, handles nested braces)
                r'((?:[^{}]*\{[^{}]*\})*[^{}]*?)'
                r'\}'                                                          # closing brace
            )
            self._function_patterns[reg_name] = re.compile(pattern, re.DOTALL)
        return self._function_patterns[reg_name]

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        '''
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        '''
        results = {}
        for path, content in self.file_contents.items():
            # Find all function definitions
            for match in re.finditer(
                r'([a-zA-Z_][a-zA-Z0-9_*\s]+)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)\s*\{',
                content, re.DOTALL
            ):
                func_start = match.start()
                func_name = match.group(2)
                # Find the function body using brace balancing
                body_start = match.end()
                brace_count = 1
                i = body_start
                while i < len(content) and brace_count > 0:
                    if content[i] == '{':
                        brace_count += 1
                    elif content[i] == '}':
                        brace_count -= 1
                    i += 1
                func_body = content[body_start:i-1]
                if re.search(r'\b' + re.escape(reg_name) + r'\b', func_body):
                    timing = self._determine_timing(func_name, func_body)
                    access_pattern = self._analyze_access_pattern(
                        func_body, reg_name)
                    results[func_name] = {
                        'file': str(path),
                        'function': func_name,
                        'timing': timing,
                        'access_pattern': access_pattern,
                    }
        return results

    def _determine_timing(self, func_name: str, func_body: str) -> str:
        '''
        Determine timing context with fallback detection.
        Args:
            func_name: Name of the function
            func_body: Content of the function
        Returns:
            Timing classification string
        '''
        # Heuristic: look for delay, wait, sleep, or comment with "timing"
        if re.search(r'\b(delay|wait|sleep)\b', func_body, re.IGNORECASE):
            return 'delayed'
        if re.search(r'//.*timing|/\*.*timing.*\*/', func_body, re.IGNORECASE | re.DOTALL):
            return 'timing_annotated'
        if re.search(r'\bISR\b|\binterrupt\b', func_name, re.IGNORECASE):
            return 'interrupt'
        return 'immediate'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        '''Analyze register access patterns within a function.'''
        # Look for read, write, modify patterns
        read_pat = re.compile(r'\b' + re.escape(reg_name) + r'\b\s*=')
        write_pat = re.compile(r'=\s*\b' + re.escape(reg_name) + r'\b')
        if read_pat.search(func_body) and write_pat.search(func_body):
            return 'read-modify-write'
        elif read_pat.search(func_body):
            return 'write'
        elif write_pat.search(func_body):
            return 'read'
        else:
            return 'unknown'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''
        Analyze register access sequences with improved function parsing.
        Enhanced to handle nested braces properly using balance counter.
        '''
        results = []
        for path, content in self.file_contents.items():
            # Find all function definitions
            for match in re.finditer(
                r'([a-zA-Z_][a-zA-Z0-9_*\s]+)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)\s*\{',
                content, re.DOTALL
            ):
                func_start = match.start()
                func_name = match.group(2)
                body_start = match.end()
                brace_count = 1
                i = body_start
                while i < len(content) and brace_count > 0:
                    if content[i] == '{':
                        brace_count += 1
                    elif content[i] == '}':
                        brace_count -= 1
                    i += 1
                func_body = content[body_start:i-1]
                accesses = []
                lines = func_body.splitlines()
                for idx, line in enumerate(lines):
                    if reg_name is None or re.search(r'\b' + re.escape(reg_name) + r'\b', line):
                        accesses.append({'line': idx+1, 'code': line.strip()})
                if accesses:
                    results.append({
                        'file': str(path),
                        'function': func_name,
                        'accesses': accesses
                    })
        return results

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''Analyze timing constraints and delays related to register accesses.'''
        results = []
        for path, content in self.file_contents.items():
            for match in re.finditer(
                r'([a-zA-Z_][a-zA-Z0-9_*\s]+)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)\s*\{',
                content, re.DOTALL
            ):
                func_name = match.group(2)
                body_start = match.end()
                brace_count = 1
                i = body_start
                while i < len(content) and brace_count > 0:
                    if content[i] == '{':
                        brace_count += 1
                    elif content[i] == '}':
                        brace_count -= 1
                    i += 1
                func_body = content[body_start:i-1]
                if reg_name is None or re.search(r'\b' + re.escape(reg_name) + r'\b', func_body):
                    delays = []
                    for m in re.finditer(r'\b(delay|wait|sleep)\s*\(([^)]*)\)', func_body, re.IGNORECASE):
                        delays.append(
                            {'type': m.group(1), 'argument': m.group(2)})
                    if delays:
                        results.append({
                            'file': str(path),
                            'function': func_name,
                            'delays': delays
                        })
        return results
