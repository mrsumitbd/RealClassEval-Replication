
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
        self._function_pattern_cache: Dict[str, re.Pattern] = {}

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        '''Get cached function pattern for register name.'''
        if reg_name not in self._function_pattern_cache:
            pattern = re.compile(
                rf'(\w+)\s*\([^)]*{re.escape(reg_name)}[^)]*\)\s*{{'
            )
            self._function_pattern_cache[reg_name] = pattern
        return self._function_pattern_cache[reg_name]

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        '''
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        '''
        results = {}
        pattern = self._get_function_pattern(reg_name)
        for file_path, content in self.file_contents.items():
            matches = pattern.finditer(content)
            for match in matches:
                func_name = match.group(1)
                func_start = match.start()
                brace_count = 1
                func_end = func_start + len(match.group(0))
                while brace_count > 0 and func_end < len(content):
                    if content[func_end] == '{':
                        brace_count += 1
                    elif content[func_end] == '}':
                        brace_count -= 1
                    func_end += 1
                func_body = content[match.start():func_end]
                timing = self._determine_timing(func_name, func_body)
                access_pattern = self._analyze_access_pattern(
                    func_body, reg_name)
                results[func_name] = {
                    'file': file_path,
                    'timing': timing,
                    'access_pattern': access_pattern
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
        if 'delay' in func_body.lower() or 'sleep' in func_body.lower():
            return 'delayed'
        elif 'interrupt' in func_name.lower():
            return 'interrupt'
        elif 'atomic' in func_name.lower() or 'spin_lock' in func_body.lower():
            return 'atomic'
        else:
            return 'immediate'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        '''Analyze register access patterns within a function.'''
        read_pattern = re.compile(
            rf'read.*{re.escape(reg_name)}', re.IGNORECASE)
        write_pattern = re.compile(
            rf'write.*{re.escape(reg_name)}', re.IGNORECASE)
        has_read = bool(read_pattern.search(func_body))
        has_write = bool(write_pattern.search(func_body))
        if has_read and has_write:
            return 'read_write'
        elif has_read:
            return 'read'
        elif has_write:
            return 'write'
        else:
            return 'unknown'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''
        Analyze register access sequences with improved function parsing.
        Enhanced to handle nested braces properly using balance counter.
        '''
        sequences = []
        for file_path, content in self.file_contents.items():
            if reg_name:
                pattern = re.compile(rf'\b{re.escape(reg_name)}\b')
            else:
                pattern = re.compile(r'\b[A-Z0-9_]+_REG\b')
            matches = pattern.finditer(content)
            for match in matches:
                pos = match.start()
                line_start = content.rfind('\n', 0, pos) + 1
                line_end = content.find('\n', pos)
                line = content[line_start:line_end].strip()
                sequences.append({
                    'file': file_path,
                    'register': match.group(0),
                    'line': line,
                    'position': pos
                })
        return sequences

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''Analyze timing constraints and delays related to register accesses.'''
        constraints = []
        for file_path, content in self.file_contents.items():
            timing_pattern = re.compile(
                r'(\bdelay\b|\bsleep\b|\bwait\b).*?(\d+)\s*(ms|us|ns)',
                re.IGNORECASE
            )
            matches = timing_pattern.finditer(content)
            for match in matches:
                constraints.append({
                    'file': file_path,
                    'constraint': match.group(0),
                    'value': match.group(2),
                    'unit': match.group(3)
                })
        return constraints
