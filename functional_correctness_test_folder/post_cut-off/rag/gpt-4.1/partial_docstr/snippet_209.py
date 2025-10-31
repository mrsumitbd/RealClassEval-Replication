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
        self._function_patterns: Dict[str, re.Pattern] = {}

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        '''Get cached function pattern for register name.'''
        if reg_name not in self._function_patterns:
            # Function pattern: matches function definitions that use reg_name in their body
            # Handles macros split across lines (with backslash or open parens)
            pattern = (
                r'(?:[a-zA-Z_][a-zA-Z0-9_*\s]+)?'  # return type
                r'\s+([a-zA-Z_][a-zA-Z0-9_]*)'      # function name
                r'\s*\([^)]*\)\s*'                  # arguments
                r'\{'                               # open brace
                # function body (non-greedy, handles nested braces poorly)
                r'((?:[^{}]|\{[^{}]*\})*)'
                r'\}'                               # close brace
            )
            self._function_patterns[reg_name] = re.compile(pattern, re.DOTALL)
        return self._function_patterns[reg_name]

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        '''
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        '''
        result = {}
        for path, content in self.file_contents.items():
            # Find all function definitions
            for match in re.finditer(
                r'(?:[a-zA-Z_][a-zA-Z0-9_*\s]+)?\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{',
                content
            ):
                func_start = match.start()
                func_name = match.group(1)
                # Find the function body using brace balancing
                body_start = content.find('{', func_start)
                if body_start == -1:
                    continue
                idx = body_start + 1
                brace_count = 1
                while idx < len(content) and brace_count > 0:
                    if content[idx] == '{':
                        brace_count += 1
                    elif content[idx] == '}':
                        brace_count -= 1
                    idx += 1
                func_body = content[body_start+1:idx-1]
                if re.search(r'\b' + re.escape(reg_name) + r'\b', func_body):
                    timing = self._determine_timing(func_name, func_body)
                    access = self._analyze_access_pattern(func_body, reg_name)
                    result = {
                        'file': str(path),
                        'function': func_name,
                        'timing': timing,
                        'access_pattern': access,
                        'body': func_body
                    }
                    return result
        return result

    def _determine_timing(self, func_name: str, func_body: str) -> str:
        '''
        Determine timing context with fallback detection.
        Args:
            func_name: Name of the function
            func_body: Content of the function
        Returns:
            Timing classification string
        '''
        # Heuristic: look for keywords in function name or body
        timing_keywords = {
            'init': 'initialization',
            'reset': 'reset',
            'irq': 'interrupt',
            'isr': 'interrupt',
            'poll': 'polling',
            'delay': 'delayed',
            'wait': 'delayed',
            'sleep': 'delayed',
            'timer': 'timed',
            'periodic': 'timed',
        }
        for key, val in timing_keywords.items():
            if key in func_name.lower():
                return val
        # Fallback: look for delay macros or functions in body
        if re.search(r'\b(delay|wait|sleep|usleep|msleep|mdelay|udelay)\b', func_body, re.IGNORECASE):
            return 'delayed'
        if re.search(r'\b(timer|periodic)\b', func_body, re.IGNORECASE):
            return 'timed'
        return 'unspecified'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        '''Analyze register access patterns within a function.'''
        # Look for read/write patterns
        # e.g., reg_name = ..., ... = reg_name, or macros like WRITE_REG(reg_name, ...)
        write_pat = re.compile(r'\b' + re.escape(reg_name) + r'\s*=')
        read_pat = re.compile(r'=\s*' + re.escape(reg_name) + r'\b')
        macro_write_pat = re.compile(
            r'\b(WRITE|SET|UPDATE)_REG\s*\(\s*' + re.escape(reg_name))
        macro_read_pat = re.compile(
            r'\b(READ|GET)_REG\s*\(\s*' + re.escape(reg_name))
        writes = len(write_pat.findall(func_body)) + \
            len(macro_write_pat.findall(func_body))
        reads = len(read_pat.findall(func_body)) + \
            len(macro_read_pat.findall(func_body))
        if writes and reads:
            return 'read/write'
        elif writes:
            return 'write'
        elif reads:
            return 'read'
        else:
            return 'unknown'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''
        Analyze register access sequences with improved function parsing.
        Enhanced to handle nested braces properly using balance counter.
        '''
        results = []
        for path, content in self.file_contents.items():
            # Find all function definitions
            for match in re.finditer(
                r'(?:[a-zA-Z_][a-zA-Z0-9_*\s]+)?\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{',
                content
            ):
                func_start = match.start()
                func_name = match.group(1)
                body_start = content.find('{', func_start)
                if body_start == -1:
                    continue
                idx = body_start + 1
                brace_count = 1
                while idx < len(content) and brace_count > 0:
                    if content[idx] == '{':
                        brace_count += 1
                    elif content[idx] == '}':
                        brace_count -= 1
                    idx += 1
                func_body = content[body_start+1:idx-1]
                if reg_name is None or re.search(r'\b' + re.escape(reg_name) + r'\b', func_body):
                    # Find all register accesses in order
                    accesses = []
                    # Simple: look for reg_name = ... or ... = reg_name
                    if reg_name:
                        access_pat = re.compile(
                            r'('
                            r'\b' + re.escape(reg_name) + r'\s*='
                            r'|=\s*' + re.escape(reg_name) + r'\b'
                            r'|\b(WRITE|SET|UPDATE)_REG\s*\(\s*' + re.escape(reg_name) +
                            r'|\b(READ|GET)_REG\s*\(\s*' + re.escape(reg_name) +
                            r')'
                        )
                    else:
                        # Any register-like identifier
                        access_pat = re.compile(
                            r'\b([A-Z_][A-Z0-9_]*)\s*='
                            r'|=\s*([A-Z_][A-Z0-9_]*)\b'
                            r'|\b(WRITE|SET|UPDATE)_REG\s*\(\s*([A-Z_][A-Z0-9_]*)'
                            r'|\b(READ|GET)_REG\s*\(\s*([A-Z_][A-Z0-9_]*)'
                        )
                    for m in access_pat.finditer(func_body):
                        accesses.append(
                            {'access': m.group(0), 'pos': m.start()})
                    results.append({
                        'file': str(path),
                        'function': func_name,
                        'accesses': accesses,
                        'body': func_body
                    })
        return results

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''Analyze timing constraints and delays related to register accesses.'''
        results = []
        delay_patterns = [
            r'\b(delay|wait|sleep|usleep|msleep|mdelay|udelay)\b',
            r'\b(timer|periodic)\b',
            r'\bDELAY_[A-Z_]+\b',
            r'\bWAIT_[A-Z_]+\b',
        ]
        delay_re = re.compile('|'.join(delay_patterns), re.IGNORECASE)
        for path, content in self.file_contents.items():
            for match in re.finditer(
                r'(?:[a-zA-Z_][a-zA-Z0-9_*\s]+)?\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{',
                content
            ):
                func_start = match.start()
                func_name = match.group(1)
                body_start = content.find('{', func_start)
                if body_start == -1:
                    continue
                idx = body_start + 1
                brace_count = 1
                while idx < len(content) and brace_count > 0:
                    if content[idx] == '{':
                        brace_count += 1
                    elif content[idx] == '}':
                        brace_count -= 1
                    idx += 1
                func_body = content[body_start+1:idx-1]
                if reg_name is None or re.search(r'\b' + re.escape(reg_name) + r'\b', func_body):
                    delays = []
                    for m in delay_re.finditer(func_body):
                        delays.append({'delay': m.group(0), 'pos': m.start()})
                    if delays:
                        results.append({
                            'file': str(path),
                            'function': func_name,
                            'delays': delays,
                            'body': func_body
                        })
        return results
