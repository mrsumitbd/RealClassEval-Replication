
import re
import pathlib
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
        self.function_patterns = {
            'function': re.compile(r'(\w+)\s*\([^)]*\)\s*\{([^}]*)\}'),
            'macro': re.compile(r'#define\s+(\w+)\s*\([^)]*\)\s*\{([^}]*)\}')
        }

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        '''Get cached function pattern for register name.'''
        return self.function_patterns.get(reg_name, None)

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        '''
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        '''
        context = {}
        for file_path, content in self.file_contents.items():
            for pattern in self.function_patterns.values():
                for match in pattern.finditer(content):
                    func_name, func_body = match.groups()
                    if reg_name in func_body:
                        timing = self._determine_timing(func_name, func_body)
                        access_pattern = self._analyze_access_pattern(
                            func_body, reg_name)
                        context[func_name] = {
                            'file_path': file_path,
                            'timing': timing,
                            'access_pattern': access_pattern
                        }
        return context

    def _determine_timing(self, func_name: str, func_body: str) -> str:
        '''
        Determine timing context with fallback detection.
        Args:
            func_name: Name of the function
            func_body: Content of the function
        Returns:
            Timing classification string
        '''
        if 'delay' in func_body or 'wait' in func_body:
            return 'delayed'
        elif 'interrupt' in func_name.lower():
            return 'interrupt'
        else:
            return 'immediate'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        '''Analyze register access patterns within a function.'''
        if f'{reg_name} = ' in func_body:
            return 'write'
        elif f' = {reg_name}' in func_body:
            return 'read'
        elif f'{reg_name} &' in func_body or f'{reg_name} |' in func_body:
            return 'modify'
        else:
            return 'unknown'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''
        Analyze register access sequences with improved function parsing.
        Enhanced to handle nested braces properly using balance counter.
        '''
        sequences = []
        for file_path, content in self.file_contents.items():
            for pattern in self.function_patterns.values():
                for match in pattern.finditer(content):
                    func_name, func_body = match.groups()
                    if reg_name is None or reg_name in func_body:
                        balance = 0
                        sequence = []
                        for line in func_body.split('\n'):
                            if '{' in line:
                                balance += line.count('{')
                            if '}' in line:
                                balance -= line.count('}')
                            if balance == 0 and reg_name in line:
                                sequence.append(line.strip())
                        if sequence:
                            sequences.append({
                                'file_path': file_path,
                                'function_name': func_name,
                                'sequence': sequence
                            })
        return sequences

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''Analyze timing constraints and delays related to register accesses.'''
        constraints = []
        for file_path, content in self.file_contents.items():
            for pattern in self.function_patterns.values():
                for match in pattern.finditer(content):
                    func_name, func_body = match.groups()
                    if reg_name is None or reg_name in func_body:
                        timing = self._determine_timing(func_name, func_body)
                        if timing != 'immediate':
                            constraints.append({
                                'file_path': file_path,
                                'function_name': func_name,
                                'timing': timing
                            })
        return constraints
