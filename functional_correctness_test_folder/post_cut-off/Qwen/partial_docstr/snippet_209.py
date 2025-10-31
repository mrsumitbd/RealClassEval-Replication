
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
        self.file_contents = file_contents
        self.pattern_cache = {}

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        '''Get cached function pattern for register name.'''
        if reg_name not in self.pattern_cache:
            pattern = re.compile(
                rf'\b\w+\s+[\w\s]+\({reg_name}\)[^{{]*{{([^}}]*)}}', re.DOTALL)
            self.pattern_cache[reg_name] = pattern
        return self.pattern_cache[reg_name]

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        '''
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        '''
        results = []
        for file_path, content in self.file_contents.items():
            pattern = self._get_function_pattern(reg_name)
            for match in pattern.finditer(content):
                func_name = content[:match.start()].rsplit(
                    '(', 1)[0].rsplit(None, 1)[-1]
                func_body = match.group(1)
                timing = self._determine_timing(func_name, func_body)
                access_pattern = self._analyze_access_pattern(
                    func_body, reg_name)
                results.append({
                    'file': str(file_path),
                    'function': func_name,
                    'body': func_body,
                    'timing': timing,
                    'access_pattern': access_pattern
                })
        return {'results': results}

    def _determine_timing(self, func_name: str, func_body: str) -> str:
        '''
        Determine timing context with fallback detection.
        Args:
            func_name: Name of the function
            func_body: Content of the function
        Returns:
            Timing classification string
        '''
        if 'wait_for_completion' in func_body:
            return 'synchronous'
        elif 'async_call' in func_body:
            return 'asynchronous'
        else:
            return 'unknown'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        '''Analyze register access patterns within a function.'''
        read_pattern = re.compile(rf'\b{reg_name}\b\s*=')
        write_pattern = re.compile(rf'\b{reg_name}\b\s*[^=]')
        reads = len(read_pattern.findall(func_body))
        writes = len(write_pattern.findall(func_body))
        if reads > 0 and writes > 0:
            return 'read-write'
        elif reads > 0:
            return 'read-only'
        elif writes > 0:
            return 'write-only'
        else:
            return 'no-access'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''
        Analyze register access sequences with improved function parsing.
        Enhanced to handle nested braces properly using balance counter.
        '''
        sequences = []
        for file_path, content in self.file_contents.items():
            if reg_name:
                pattern = self._get_function_pattern(reg_name)
            else:
                pattern = re.compile(
                    r'\b\w+\s+[\w\s]+\([^)]*\)[^{{]*{{([^}}]*)}}', re.DOTALL)
            for match in pattern.finditer(content):
                func_name = content[:match.start()].rsplit(
                    '(', 1)[0].rsplit(None, 1)[-1]
                func_body = match.group(1)
                balance = 0
                sequence = []
                for line in func_body.splitlines():
                    balance += line.count('{') - line.count('}')
                    if reg_name is None or reg_name in line:
                        sequence.append(line.strip())
                    if balance <= 0 and sequence:
                        sequences.append({
                            'file': str(file_path),
                            'function': func_name,
                            'sequence': sequence
                        })
                        sequence = []
        return sequences

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''Analyze timing constraints and delays related to register accesses.'''
        constraints = []
        for file_path, content in self.file_contents.items():
            if reg_name:
                pattern = self._get_function_pattern(reg_name)
            else:
                pattern = re.compile(
                    r'\b\w+\s+[\w\s]+\([^)]*\)[^{{]*{{([^}}]*)}}', re.DOTALL)
            for match in pattern.finditer(content):
                func_name = content[:match.start()].rsplit(
                    '(', 1)[0].rsplit(None, 1)[-1]
                func_body = match.group(1)
                delay_pattern = re.compile(r'\bdelay\((\d+)\)')
                delays = delay_pattern.findall(func_body)
                if delays:
                    constraints.append({
                        'file': str(file_path),
                        'function': func_name,
                        'delays': [int(d) for d in delays]
                    })
        return constraints
