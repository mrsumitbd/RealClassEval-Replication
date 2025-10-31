
import pathlib
import re
from typing import Dict, List, Any, Optional


class DriverAnalyzer:
    '''
    Encapsulates driver analysis functionality with shared state.
    This class maintains pre-compiled regex patterns and file content
    to avoid duplication and improve performance.
    '''

    def __init__(self, file_contents: Dict[pathlib.Path, str]):
        self.file_contents = file_contents
        self.function_patterns = {
            'function': re.compile(r'(\w+)\s*\([^)]*\)\s*\{([^}]*)\}'),
            'macro': re.compile(r'#define\s+(\w+)\s*\([^)]*\)\s*\{([^}]*)\}'),
        }
        self.timing_keywords = {
            'posedge': re.compile(r'posedge\s+\w+'),
            'negedge': re.compile(r'negedge\s+\w+'),
            'always': re.compile(r'always\s+@\s*\([^)]*\)'),
        }
        self.access_patterns = {
            'read': re.compile(r'\w+\s*=\s*\w+'),
            'write': re.compile(r'\w+\s*=\s*[^;]+;'),
        }

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        '''Get cached function pattern for register name.'''
        return self.function_patterns.get(reg_name, self.function_patterns['function'])

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        '''
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        '''
        function_context = {}
        for file_path, content in self.file_contents.items():
            pattern = self._get_function_pattern(reg_name)
            matches = pattern.finditer(content)
            for match in matches:
                func_name, func_body = match.groups()
                if reg_name in func_body:
                    timing = self._determine_timing(func_name, func_body)
                    access_pattern = self._analyze_access_pattern(
                        func_body, reg_name)
                    function_context[func_name] = {
                        'file_path': file_path,
                        'timing': timing,
                        'access_pattern': access_pattern,
                    }
        return function_context

    def _determine_timing(self, func_name: str, func_body: str) -> str:
        '''
        Determine timing context with fallback detection.
        Args:
            func_name: Name of the function
            func_body: Content of the function
        Returns:
            Timing classification string
        '''
        for keyword, pattern in self.timing_keywords.items():
            if pattern.search(func_body):
                return keyword
        return 'unknown'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        '''Analyze register access patterns within a function.'''
        for pattern_name, pattern in self.access_patterns.items():
            if pattern.search(func_body):
                return pattern_name
        return 'unknown'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''
        Analyze register access sequences with improved function parsing.
        Enhanced to handle nested braces properly using balance counter.
        '''
        access_sequences = []
        for file_path, content in self.file_contents.items():
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if reg_name and reg_name not in line:
                    continue
                brace_balance = line.count('{') - line.count('}')
                if brace_balance > 0:
                    j = i + 1
                    while j < len(lines) and brace_balance > 0:
                        brace_balance += lines[j].count(
                            '{') - lines[j].count('}')
                        j += 1
                    sequence = '\n'.join(lines[i:j])
                    access_sequences.append({
                        'file_path': file_path,
                        'line_number': i + 1,
                        'sequence': sequence,
                    })
        return access_sequences

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''Analyze timing constraints and delays related to register accesses.'''
        timing_constraints = []
        for file_path, content in self.file_contents.items():
            for keyword, pattern in self.timing_keywords.items():
                matches = pattern.finditer(content)
                for match in matches:
                    if reg_name and reg_name not in match.group():
                        continue
                    timing_constraints.append({
                        'file_path': file_path,
                        'keyword': keyword,
                        'constraint': match.group(),
                    })
        return timing_constraints
