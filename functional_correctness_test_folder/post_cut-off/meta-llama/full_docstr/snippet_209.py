
import pathlib
import re
from typing import Dict, Any, List, Optional


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
        self.function_patterns = {}

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        '''Get cached function pattern for register name.'''
        if reg_name not in self.function_patterns:
            self.function_patterns[reg_name] = re.compile(
                rf'\b\w+\s+({reg_name})\b')
        return self.function_patterns[reg_name]

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        '''
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        '''
        results = {}
        pattern = self._get_function_pattern(reg_name)
        for file_path, content in self.file_contents.items():
            for match in pattern.finditer(content):
                func_name = self._extract_function_name(content, match.start())
                func_body = self._extract_function_body(content, match.start())
                timing = self._determine_timing(func_name, func_body)
                results[str(file_path)] = {
                    'function_name': func_name,
                    'register_name': reg_name,
                    'timing': timing,
                    'access_pattern': self._analyze_access_pattern(func_body, reg_name)
                }
        return results

    def _extract_function_name(self, content: str, pos: int) -> str:
        '''Extract function name from content at given position.'''
        start = content.rfind('(', 0, pos)
        if start == -1:
            return 'unknown'
        start = content.rfind(' ', 0, start)
        if start == -1:
            start = 0
        else:
            start += 1
        end = content.find('(', start)
        return content[start:end].strip()

    def _extract_function_body(self, content: str, pos: int) -> str:
        '''Extract function body from content at given position.'''
        start = content.find('{', pos)
        if start == -1:
            return ''
        balance = 1
        end = start + 1
        while balance > 0 and end < len(content):
            if content[end] == '{':
                balance += 1
            elif content[end] == '}':
                balance -= 1
            end += 1
        return content[start+1:end-1]

    def _determine_timing(self, func_name: str, func_body: str) -> str:
        '''
        Determine timing context with fallback detection.
        Args:
            func_name: Name of the function
            func_body: Content of the function
        Returns:
            Timing classification string
        '''
        # Simple fallback detection for demonstration
        if 'delay' in func_body.lower() or 'sleep' in func_body.lower():
            return 'delayed'
        elif 'interrupt' in func_name.lower():
            return 'interrupt'
        else:
            return 'normal'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        '''Analyze register access patterns within a function.'''
        # Simple pattern analysis for demonstration
        read_pattern = re.compile(rf'{reg_name}\s*=\s*\w+')
        write_pattern = re.compile(rf'\w+\s*=\s*{reg_name}')
        if read_pattern.search(func_body) and write_pattern.search(func_body):
            return 'read_write'
        elif read_pattern.search(func_body):
            return 'read'
        elif write_pattern.search(func_body):
            return 'write'
        else:
            return 'unknown'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''
        Analyze register access sequences with improved function parsing.
        Enhanced to handle nested braces properly using balance counter.
        '''
        results = []
        for file_path, content in self.file_contents.items():
            accesses = []
            for match in re.finditer(rf'\b{reg_name}\b', content) if reg_name else []:
                func_name = self._extract_function_name(content, match.start())
                func_body = self._extract_function_body(content, match.start())
                accesses.append({
                    'file_path': str(file_path),
                    'function_name': func_name,
                    'register_name': reg_name,
                    'access_type': self._analyze_access_pattern(func_body, reg_name) if reg_name else 'unknown'
                })
            results.extend(accesses)
        return results

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''Analyze timing constraints and delays related to register accesses.'''
        results = []
        for file_path, content in self.file_contents.items():
            for match in re.finditer(rf'\b{reg_name}\b', content) if reg_name else []:
                func_name = self._extract_function_name(content, match.start())
                func_body = self._extract_function_body(content, match.start())
                timing = self._determine_timing(func_name, func_body)
                results.append({
                    'file_path': str(file_path),
                    'function_name': func_name,
                    'register_name': reg_name,
                    'timing': timing
                })
        return results
