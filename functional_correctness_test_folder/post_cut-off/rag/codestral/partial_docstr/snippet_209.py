
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
        self._function_patterns = {}
        self._function_pattern = re.compile(
            r'^\s*(?:inline\s+)?(?:static\s+)?(?:void|int|bool|uint\d+_t)\s+(\w+)\s*\([^)]*\)\s*\{',
            re.MULTILINE
        )
        self._macro_pattern = re.compile(
            r'^\s*#define\s+(\w+)\s*\([^)]*\)\s*\{',
            re.MULTILINE
        )
        self._timing_keywords = {
            'early': ['early', 'pre', 'before'],
            'late': ['late', 'post', 'after'],
            'critical': ['critical', 'sensitive', 'timing']
        }

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        '''Get cached function pattern for register name.'''
        if reg_name not in self._function_patterns:
            self._function_patterns[reg_name] = re.compile(
                rf'\b{reg_name}\b.*?\{{.*?\}}',
                re.DOTALL
            )
        return self._function_patterns[reg_name]

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        '''
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        '''
        results = []
        for file_path, content in self.file_contents.items():
            # Find all functions containing the register
            for match in self._function_pattern.finditer(content):
                func_name = match.group(1)
                start_pos = match.end()
                brace_count = 1
                func_body = ''

                # Extract function body
                while brace_count > 0 and start_pos < len(content):
                    char = content[start_pos]
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                    func_body += char
                    start_pos += 1

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

            # Check for macros containing the register
            for match in self._macro_pattern.finditer(content):
                macro_name = match.group(1)
                start_pos = match.end()
                brace_count = 1
                macro_body = ''

                # Extract macro body
                while brace_count > 0 and start_pos < len(content):
                    char = content[start_pos]
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                    macro_body += char
                    start_pos += 1

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
        for timing, keywords in self._timing_keywords.items():
            for keyword in keywords:
                if keyword in func_name.lower() or keyword in func_body.lower():
                    return timing

        # Fallback to function name patterns
        if 'early' in func_name.lower():
            return 'early'
        elif 'late' in func_name.lower():
            return 'late'
        elif 'critical' in func_name.lower():
            return 'critical'

        return 'unknown'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        '''Analyze register access patterns within a function.'''
        read_pattern = re.compile(rf'\b{reg_name}\b\s*=\s*\w+')
        write_pattern = re.compile(rf'\w+\s*=\s*\b{reg_name}\b')
        read_write_pattern = re.compile(
            rf'\b{reg_name}\b\s*=\s*\w+\s*;\s*\w+\s*=\s*\b{reg_name}\b')

        if read_write_pattern.search(func_body):
            return 'read_write'
        elif write_pattern.search(func_body):
            return 'write'
        elif read_pattern.search(func_body):
            return 'read'
        else:
            return 'unknown'

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
                pattern = self._function_pattern

            for match in pattern.finditer(content):
                func_name = match.group(1)
                start_pos = match.end()
                brace_count = 1
                func_body = ''

                # Extract function body with proper brace balancing
                while brace_count > 0 and start_pos < len(content):
                    char = content[start_pos]
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                    func_body += char
                    start_pos += 1

                if reg_name and reg_name not in func_body:
                    continue

                # Analyze access sequences
                accesses = []
                for line in func_body.split('\n'):
                    if reg_name and reg_name in line:
                        access_type = 'read' if '=' in line.split(reg_name)[
                            0] else 'write'
                        accesses.append({
                            'line': line.strip(),
                            'type': access_type
                        })

                if accesses:
                    results.append({
                        'file': str(file_path),
                        'function': func_name,
                        'accesses': accesses
                    })

        return results

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''Analyze timing constraints and delays related to register accesses.'''
        results = []
        delay_pattern = re.compile(
            r'\b(?:delay|wait|usleep|sleep|nanosleep)\b')

        for file_path, content in self.file_contents.items():
            if reg_name:
                pattern = self._get_function_pattern(reg_name)
            else:
                pattern = self._function_pattern

            for match in pattern.finditer(content):
                func_name = match.group(1)
                start_pos = match.end()
                brace_count = 1
                func_body = ''

                # Extract function body
                while brace_count > 0 and start_pos < len(content):
                    char = content[start_pos]
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                    func_body += char
                    start_pos += 1

                if reg_name and reg_name not in func_body:
                    continue

                # Find delays and timing constraints
                delays = []
                for line in func_body.split('\n'):
                    if delay_pattern.search(line):
                        delays.append(line.strip())

                if delays:
                    timing = self._determine_timing(func_name, func_body)
                    results.append({
                        'file': str(file_path),
                        'function': func_name,
                        'timing': timing,
                        'delays': delays
                    })

        return results
