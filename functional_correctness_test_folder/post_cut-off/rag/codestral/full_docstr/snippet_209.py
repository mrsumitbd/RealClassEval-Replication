
import pathlib
import re
from typing import Any, Dict, List, Optional


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
        self.function_pattern = re.compile(
            r'^\s*(?:inline\s+)?(?:static\s+)?(?:void|int|unsigned|signed|char|short|long|float|double|bool)\s+'
            r'(\w+)\s*\([^)]*\)\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}',
            re.MULTILINE
        )
        self.macro_pattern = re.compile(
            r'^\s*#define\s+(\w+)\s*\(([^)]*)\)\s*([^{]*(?:\{[^{}]*\}[^{}]*)*)',
            re.MULTILINE
        )
        self.register_access_pattern = re.compile(
            r'\b(?:read|write|set|clear|toggle)\s+(\w+)\b',
            re.IGNORECASE
        )
        self.timing_keywords = {
            'delay', 'wait', 'timeout', 'poll', 'clock', 'cycle', 'period'
        }

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        '''Get cached function pattern for register name.'''
        if reg_name not in self.function_patterns:
            self.function_patterns[reg_name] = re.compile(
                fr'\b{reg_name}\b.*?\b(?:read|write|set|clear|toggle)\b',
                re.IGNORECASE | re.DOTALL
            )
        return self.function_patterns[reg_name]

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        '''
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        '''
        results = []
        for file_path, content in self.file_contents.items():
            # Analyze functions
            for match in self.function_pattern.finditer(content):
                func_name, func_body = match.groups()
                if reg_name in func_body:
                    timing = self._determine_timing(func_name, func_body)
                    access_pattern = self._analyze_access_pattern(
                        func_body, reg_name)
                    results.append({
                        'file': str(file_path),
                        'function': func_name,
                        'timing': timing,
                        'access_pattern': access_pattern
                    })

            # Analyze macros
            for match in self.macro_pattern.finditer(content):
                macro_name, params, macro_body = match.groups()
                if reg_name in macro_body:
                    timing = self._determine_timing(macro_name, macro_body)
                    access_pattern = self._analyze_access_pattern(
                        macro_body, reg_name)
                    results.append({
                        'file': str(file_path),
                        'macro': macro_name,
                        'timing': timing,
                        'access_pattern': access_pattern
                    })

        return {
            'register': reg_name,
            'contexts': results
        }

    def _determine_timing(self, func_name: str, func_body: str) -> str:
        '''
        Determine timing context with fallback detection.
        Args:
            func_name: Name of the function
            func_body: Content of the function
        Returns:
            Timing classification string
        '''
        # Check for explicit timing keywords
        for keyword in self.timing_keywords:
            if keyword in func_body.lower():
                return f'explicit_{keyword}'

        # Check for common timing patterns
        if 'for (' in func_body or 'while (' in func_body:
            return 'loop_based'
        elif 'if (' in func_body:
            return 'conditional'
        else:
            return 'direct_access'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        '''Analyze register access patterns within a function.'''
        accesses = []
        for match in self.register_access_pattern.finditer(func_body):
            access_type = match.group(0).lower()
            accesses.append(access_type)

        if not accesses:
            return 'unknown'

        if len(accesses) == 1:
            return accesses[0]

        if all(a == accesses[0] for a in accesses):
            return f'multiple_{accesses[0]}'

        return 'mixed_access'

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
                pattern = self.register_access_pattern

            for match in pattern.finditer(content):
                if reg_name:
                    reg_name_match = match.group(1)
                    if reg_name and reg_name != reg_name_match:
                        continue

                # Extract the function body with proper brace balancing
                brace_balance = 0
                start_pos = match.start()
                end_pos = start_pos
                for i, char in enumerate(content[start_pos:], start_pos):
                    if char == '{':
                        brace_balance += 1
                    elif char == '}':
                        brace_balance -= 1
                        if brace_balance == 0:
                            end_pos = i + 1
                            break

                func_body = content[start_pos:end_pos]
                results.append({
                    'file': str(file_path),
                    'register': reg_name_match if reg_name else reg_name,
                    'access_sequence': func_body.strip()
                })

        return results

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''Analyze timing constraints and delays related to register accesses.'''
        results = []
        for file_path, content in self.file_contents.items():
            for match in self.function_pattern.finditer(content):
                func_name, func_body = match.groups()
                if reg_name and reg_name not in func_body:
                    continue

                timing = self._determine_timing(func_name, func_body)
                if timing != 'direct_access':
                    results.append({
                        'file': str(file_path),
                        'function': func_name,
                        'timing': timing,
                        'register': reg_name if reg_name else 'any'
                    })

        return results
