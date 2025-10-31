
import re
import pathlib
from typing import Dict, Any, List, Optional, Pattern


class DriverAnalyzer:
    '''
    Encapsulates driver analysis functionality with shared state.
    This class maintains pre-compiled regex patterns and file content
    to avoid duplication and improve performance.
    '''

    def __init__(self, file_contents: Dict[pathlib.Path, str]):
        self.file_contents = file_contents
        self._pattern_cache: Dict[str, Pattern] = {}

    def _get_function_pattern(self, reg_name: str) -> Pattern:
        '''Get cached function pattern for register name.'''
        key = f'func_{reg_name}'
        if key not in self._pattern_cache:
            # Matches a function or task definition that contains the register name
            # Handles multi-line signatures and bodies
            pattern = rf'''
                (?:module|task|function)\s+[\w]+\s*   # module/task/function keyword
                [\w]*\s*                             # optional name
                \([^)]*\)\s*                         # optional arguments
                (?:#\s*\([^\)]*\)\s*)?               # optional parameter list
                (?:\s*;\s*)?                         # optional semicolon
                (?:\s*begin\s*)?                     # optional begin
                (?P<body>[^;]*?)                     # body up to first semicolon
                (?:;|end\s*function|end\s*task|end\s*module)  # end of block
            '''
            self._pattern_cache[key] = re.compile(
                pattern, re.IGNORECASE | re.DOTALL | re.VERBOSE)
        return self._pattern_cache[key]

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        '''
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        '''
        results = {}
        pattern = self._get_function_pattern(reg_name)
        for path, content in self.file_contents.items():
            for match in pattern.finditer(content):
                body = match.group('body')
                # Find function name if present
                name_match = re.search(
                    r'(?:module|task|function)\s+(\w+)', match.group(0), re.IGNORECASE)
                func_name = name_match.group(1) if name_match else 'unknown'
                timing = self._determine_timing(func_name, body)
                results[path] = {
                    'function': func_name,
                    'body': body,
                    'timing': timing
                }
                # Only first occurrence per file
                break
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
        # Look for edge-sensitive constructs
        if re.search(r'@(posedge|negedge)', func_body, re.IGNORECASE):
            return 'edge-sensitive'
        if re.search(r'always\s*@\s*\(.*\)', func_body, re.IGNORECASE):
            return 'always'
        # Fallback: if no explicit edge, assume combinational
        return 'combinational'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        '''Analyze register access patterns within a function.'''
        # Write: <= or = on left side
        write = re.search(rf'{re.escape(reg_name)}\s*(?:<=|=)', func_body)
        # Read: reg_name on right side of assignment or in expression
        read = re.search(rf'(?<![<>=])\b{re.escape(reg_name)}\b', func_body)
        if write and read:
            return 'read_write'
        if write:
            return 'write'
        if read:
            return 'read'
        return 'none'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''
        Analyze register access sequences with improved function parsing.
        Enhanced to handle nested braces properly using balance counter.
        '''
        results: List[Dict[str, Any]] = []
        for path, content in self.file_contents.items():
            # Find all function/task/module definitions
            func_pattern = re.compile(
                r'(?:module|task|function)\s+[\w]+\s*\([^)]*\)\s*;?\s*(?:begin\s*)?', re.IGNORECASE)
            for m in func_pattern.finditer(content):
                start = m.end()
                # Find matching end using balance counter
                balance = 0
                i = start
                while i < len(content):
                    if content[i:i+5] == 'begin':
                        balance += 1
                        i += 5
                    elif content[i:i+3] == 'end':
                        balance -= 1
                        i += 3
                        if balance == 0:
                            break
                    else:
                        i += 1
                body = content[start:i]
                # Find all accesses to reg_name if specified
                if reg_name:
                    accesses = re.finditer(rf'\b{re.escape(reg_name)}\b', body)
                else:
                    # dummy to iterate over all words
                    accesses = re.finditer(r'\b\w+\b', body)
                for acc in accesses:
                    if reg_name and acc.group(0) != reg_name:
                        continue
                    line_no = body[:acc.start()].count('\n') + 1
                    access_type = self._analyze_access_pattern(
                        body, reg_name) if reg_name else 'unknown'
                    results.append({
                        'file': path,
                        'function': m.group(0).split()[1] if len(m.group(0).split()) > 1 else 'unknown',
                        'reg': reg_name,
                        'line': line_no,
                        'access_type': access_type
                    })
        return results

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''Analyze timing constraints and delays related to register accesses.'''
        results: List[Dict[str, Any]] = []
        delay_pattern = re.compile(r'#\s*(\d+(\.\d+)?)')
        for path, content in self.file_contents.items():
            for m in delay_pattern.finditer(content):
                delay = float(m.group(1))
                # Find surrounding function
                func_start = content.rfind('function', 0, m.start())
                func_end = content.find('end', m.end())
                func_name = 'unknown'
                if func_start != -1:
                    func_name = re.search(
                        r'function\s+(\w+)', content[func_start:func_end], re.IGNORECASE)
                    func_name = func_name.group(1) if func_name else 'unknown'
                results.append({
                    'file': path,
                    'function': func_name,
                    'delay_ns': delay,
                    'reg': reg_name
                })
        return results
