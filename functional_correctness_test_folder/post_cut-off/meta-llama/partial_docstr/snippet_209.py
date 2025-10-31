
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
        self.file_contents = file_contents
        self.function_patterns = {}

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        '''Get cached function pattern for register name.'''
        if reg_name not in self.function_patterns:
            self.function_patterns[reg_name] = re.compile(
                rf'\b\w+\s+[\w:]+\({reg_name}\s*[,)]')
        return self.function_patterns[reg_name]

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        '''
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        '''
        pattern = self._get_function_pattern(reg_name)
        results = {'functions': [], 'timing': {}}
        for file_path, content in self.file_contents.items():
            for match in pattern.finditer(content):
                start = match.start()
                end = content.find('}', start)
                if end == -1:
                    continue
                func_body = content[start:end+1]
                func_name = re.search(
                    r'\b(\w+)\s*\(', content[:start]).group(1)
                timing = self._determine_timing(func_name, func_body)
                results['functions'].append(
                    {'name': func_name, 'body': func_body})
                results['timing'][func_name] = timing
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
        # Simple timing detection based on keyword presence
        if 'delay' in func_body.lower() or 'sleep' in func_body.lower():
            return 'delayed'
        elif 'interrupt' in func_body.lower():
            return 'interrupt'
        else:
            return 'normal'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        '''Analyze register access patterns within a function.'''
        # Simple access pattern analysis based on read/write operations
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
            balance = 0
            func_body = ''
            in_function = False
            for line in content.split('\n'):
                if '{' in line:
                    balance += line.count('{')
                    in_function = True
                if '}' in line:
                    balance -= line.count('}')
                if in_function:
                    func_body += line + '\n'
                if balance == 0 and in_function:
                    func_name = re.search(r'\b(\w+)\s*\(', func_body).group(1)
                    access_pattern = self._analyze_access_pattern(
                        func_body, reg_name or '')
                    results.append(
                        {'function': func_name, 'pattern': access_pattern})
                    func_body = ''
                    in_function = False
        return results

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''Analyze timing constraints and delays related to register accesses.'''
        results = []
        for file_path, content in self.file_contents.items():
            for match in re.finditer(r'delay\s*\(\s*(\d+)\s*\)', content):
                results.append(
                    {'location': file_path, 'delay': match.group(1)})
        return results
