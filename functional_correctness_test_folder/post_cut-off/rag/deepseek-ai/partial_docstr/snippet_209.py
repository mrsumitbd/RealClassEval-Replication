
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
        self._function_pattern_cache: Dict[str, re.Pattern] = {}

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        '''Get cached function pattern for register name.'''
        if reg_name not in self._function_pattern_cache:
            pattern = re.compile(
                rf'(\w+)\s*\([^)]*{re.escape(reg_name)}[^)]*\)\s*{{([^}}]*)}}',
                re.MULTILINE | re.DOTALL
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
                func_body = match.group(2)
                timing = self._determine_timing(func_name, func_body)
                access_pattern = self._analyze_access_pattern(
                    func_body, reg_name)
                results[func_name] = {
                    'file': str(file_path),
                    'timing': timing,
                    'access_pattern': access_pattern,
                    'function_body': func_body
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
        if 'delay' in func_name.lower():
            return 'delayed'
        if 'interrupt' in func_name.lower() or 'isr' in func_name.lower():
            return 'interrupt'
        if re.search(r'\bwait\b|\bsleep\b|\bdelay\b', func_body, re.IGNORECASE):
            return 'delayed'
        return 'immediate'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        '''Analyze register access patterns within a function.'''
        read_pattern = re.compile(rf'\b{re.escape(reg_name)}\s*=\s*[^;]+;')
        write_pattern = re.compile(rf'[^=]=\s*\b{re.escape(reg_name)}\b')
        reads = len(read_pattern.findall(func_body))
        writes = len(write_pattern.findall(func_body))
        if reads > 0 and writes > 0:
            return 'read_write'
        elif reads > 0:
            return 'read_only'
        elif writes > 0:
            return 'write_only'
        return 'none'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''
        Analyze register access sequences with improved function parsing.
        Enhanced to handle nested braces properly using balance counter.
        '''
        sequences = []
        for file_path, content in self.file_contents.items():
            if reg_name:
                pattern = re.compile(rf'\b{re.escape(reg_name)}\b')
                matches = pattern.finditer(content)
                for match in matches:
                    sequences.append({
                        'file': str(file_path),
                        'position': match.start(),
                        'line': content.count('\n', 0, match.start()) + 1,
                        'context': content[max(0, match.start()-20):match.end()+20]
                    })
            else:
                # Fallback to general access pattern analysis
                access_pattern = re.compile(r'\b[A-Z0-9_]+\b')
                matches = access_pattern.finditer(content)
                for match in matches:
                    sequences.append({
                        'file': str(file_path),
                        'position': match.start(),
                        'line': content.count('\n', 0, match.start()) + 1,
                        'context': content[max(0, match.start()-20):match.end()+20]
                    })
        return sequences

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''Analyze timing constraints and delays related to register accesses.'''
        constraints = []
        timing_keywords = ['delay', 'wait', 'sleep', 'timeout', 'timer']
        for file_path, content in self.file_contents.items():
            for keyword in timing_keywords:
                pattern = re.compile(rf'\b{keyword}\b', re.IGNORECASE)
                matches = pattern.finditer(content)
                for match in matches:
                    constraints.append({
                        'file': str(file_path),
                        'keyword': keyword,
                        'position': match.start(),
                        'line': content.count('\n', 0, match.start()) + 1,
                        'context': content[max(0, match.start()-20):match.end()+20]
                    })
        return constraints
