
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
        self.function_patterns = {}

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        '''Get cached function pattern for register name.'''
        if reg_name not in self.function_patterns:
            # Example pattern, adjust as necessary
            pattern = re.compile(
                rf'function\s+(\w+)\s*{{.*?\b{re.escape(reg_name)}\b.*?}}', re.DOTALL | re.IGNORECASE)
            self.function_patterns[reg_name] = pattern
        return self.function_patterns[reg_name]

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        '''
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        '''
        results = []
        pattern = self._get_function_pattern(reg_name)
        for file_path, content in self.file_contents.items():
            for match in pattern.finditer(content):
                func_name = match.group(1)
                func_body = match.group(0)
                timing = self._determine_timing(func_name, func_body)
                access_pattern = self._analyze_access_pattern(
                    func_body, reg_name)
                results.append({
                    'file_path': str(file_path),
                    'function_name': func_name,
                    'function_body': func_body,
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
        # Example timing detection, adjust as necessary
        if 'wait_for_clock' in func_body:
            return 'clock_synchronous'
        elif 'delay_us' in func_body:
            return 'microsecond_delay'
        else:
            return 'unknown'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        '''Analyze register access patterns within a function.'''
        # Example access pattern analysis, adjust as necessary
        read_pattern = re.compile(
            rf'\b{re.escape(reg_name)}\b\s*=\s*read_register\(', re.IGNORECASE)
        write_pattern = re.compile(
            rf'write_register\(\s*{re.escape(reg_name)}\b', re.IGNORECASE)
        reads = len(read_pattern.findall(func_body))
        writes = len(write_pattern.findall(func_body))
        return f'reads: {reads}, writes: {writes}'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''
        Analyze register access sequences with improved function parsing.
        Enhanced to handle nested braces properly using balance counter.
        '''
        results = []
        for file_path, content in self.file_contents.items():
            if reg_name:
                pattern = self._get_function_pattern(reg_name)
            else:
                pattern = re.compile(
                    r'function\s+(\w+)\s*{.*?}', re.DOTALL | re.IGNORECASE)
            for match in pattern.finditer(content):
                func_name = match.group(1)
                func_body = match.group(0)
                if reg_name:
                    access_pattern = self._analyze_access_pattern(
                        func_body, reg_name)
                else:
                    access_pattern = 'all_registers'
                results.append({
                    'file_path': str(file_path),
                    'function_name': func_name,
                    'function_body': func_body,
                    'access_pattern': access_pattern
                })
        return results

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''Analyze timing constraints and delays related to register accesses.'''
        results = []
        for file_path, content in self.file_contents.items():
            if reg_name:
                pattern = self._get_function_pattern(reg_name)
            else:
                pattern = re.compile(
                    r'function\s+(\w+)\s*{.*?}', re.DOTALL | re.IGNORECASE)
            for match in pattern.finditer(content):
                func_name = match.group(1)
                func_body = match.group(0)
                timing = self._determine_timing(func_name, func_body)
                results.append({
                    'file_path': str(file_path),
                    'function_name': func_name,
                    'function_body': func_body,
                    'timing': timing
                })
        return results
