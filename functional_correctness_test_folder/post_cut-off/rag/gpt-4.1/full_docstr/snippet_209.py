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
            # Handles macros split across lines (with backslash)
            pattern = (
                r'(?:[a-zA-Z_][a-zA-Z0-9_*\s]+)?'   # return type (optional)
                r'([a-zA-Z_][a-zA-Z0-9_]*)'         # function name
                r'\s*\([^)]*\)\s*'                  # arguments
                r'\{'                               # opening brace
                # function body (non-greedy, handles nested braces poorly)
                r'((?:[^{}]|\{[^{}]*\})*)'
                r'\}'                               # closing brace
            )
            self._function_patterns[reg_name] = re.compile(pattern, re.DOTALL)
        return self._function_patterns[reg_name]

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        '''
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        '''
        results = {}
        for path, content in self.file_contents.items():
            for func in self._extract_functions(content):
                func_name, func_body = func['name'], func['body']
                if self._reg_in_body(reg_name, func_body):
                    timing = self._determine_timing(func_name, func_body)
                    access = self._analyze_access_pattern(func_body, reg_name)
                    results[func_name] = {
                        'file': str(path),
                        'timing': timing,
                        'access_pattern': access,
                        'body': func_body
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
        # Heuristic: look for keywords in function name or body
        timing_keywords = {
            'init': 'initialization',
            'probe': 'initialization',
            'exit': 'shutdown',
            'remove': 'shutdown',
            'irq': 'interrupt',
            'isr': 'interrupt',
            'poll': 'polling',
            'timer': 'timer',
            'delay': 'delayed',
            'sleep': 'delayed',
            'wait': 'delayed',
            'thread': 'threaded',
            'work': 'workqueue',
        }
        for key, val in timing_keywords.items():
            if key in func_name.lower():
                return val
        # Fallback: look for timing-related calls in body
        if re.search(r'\b(msleep|udelay|mdelay|schedule_timeout|wait_event)\b', func_body):
            return 'delayed'
        if re.search(r'\b(request_irq|free_irq|enable_irq|disable_irq)\b', func_body):
            return 'interrupt'
        if re.search(r'\bthread|kthread_run|workqueue|queue_work\b', func_body):
            return 'threaded'
        return 'unknown'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        '''Analyze register access patterns within a function.'''
        # Look for read/write macros or direct access
        patterns = [
            rf'\bwrite.*\(\s*{re.escape(reg_name)}\b',
            rf'\bread.*\(\s*{re.escape(reg_name)}\b',
            rf'{re.escape(reg_name)}\s*=',  # assignment
            rf'=\s*{re.escape(reg_name)}\b',  # used in assignment
        ]
        for pat in patterns:
            if re.search(pat, func_body):
                if 'write' in pat:
                    return 'write'
                elif 'read' in pat:
                    return 'read'
                elif '=' in pat:
                    return 'assignment'
        return 'unknown'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''
        Analyze register access sequences with improved function parsing.
        Enhanced to handle nested braces properly using balance counter.
        '''
        results = []
        for path, content in self.file_contents.items():
            for func in self._extract_functions(content):
                func_name, func_body = func['name'], func['body']
                if reg_name is None or self._reg_in_body(reg_name, func_body):
                    accesses = self._find_reg_accesses(func_body, reg_name)
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
        for path, content in self.file_contents.items():
            for func in self._extract_functions(content):
                func_name, func_body = func['name'], func['body']
                if reg_name is None or self._reg_in_body(reg_name, func_body):
                    delays = self._find_delays(func_body)
                    results.append({
                        'file': str(path),
                        'function': func_name,
                        'delays': delays,
                        'body': func_body
                    })
        return results

    def _extract_functions(self, content: str) -> List[Dict[str, str]]:
        '''
        Extract functions from C source code, handling nested braces.
        Returns list of dicts: {'name': ..., 'body': ...}
        '''
        functions = []
        func_pattern = re.compile(
            r'([a-zA-Z_][a-zA-Z0-9_*\s]+)?'   # return type (optional)
            r'([a-zA-Z_][a-zA-Z0-9_]*)'       # function name
            r'\s*\([^)]*\)\s*'                # arguments
            r'\{',                            # opening brace
            re.MULTILINE
        )
        pos = 0
        while True:
            m = func_pattern.search(content, pos)
            if not m:
                break
            func_name = m.group(2)
            brace_start = m.end() - 1
            brace_end = self._find_matching_brace(content, brace_start)
            if brace_end == -1:
                break
            func_body = content[brace_start+1:brace_end]
            functions.append({'name': func_name, 'body': func_body})
            pos = brace_end + 1
        return functions

    def _find_matching_brace(self, text: str, start: int) -> int:
        '''
        Find the position of the matching closing brace for the opening brace at start.
        Returns -1 if not found.
        '''
        count = 0
        for i in range(start, len(text)):
            if text[i] == '{':
                count += 1
            elif text[i] == '}':
                count -= 1
                if count == 0:
                    return i
        return -1

    def _reg_in_body(self, reg_name: str, body: str) -> bool:
        # Accepts macro splits (backslash-newline)
        reg_pat = re.compile(
            rf'{re.escape(reg_name)}(?:\s*\\\s*\n\s*)?', re.MULTILINE)
        return bool(reg_pat.search(body))

    def _find_reg_accesses(self, body: str, reg_name: Optional[str]) -> List[Dict[str, Any]]:
        '''
        Find all accesses to reg_name in the function body.
        If reg_name is None, find all register-like accesses.
        '''
        accesses = []
        if reg_name:
            pat = re.compile(
                rf'\b(read|write)[a-zA-Z0-9_]*\s*\(\s*{re.escape(reg_name)}\b.*?\)', re.DOTALL)
            for m in pat.finditer(body):
                accesses.append(
                    {'type': m.group(1), 'text': m.group(0), 'start': m.start()})
        else:
            pat = re.compile(
                r'\b(read|write)[a-zA-Z0-9_]*\s*\(\s*([A-Z0-9_]+)\b.*?\)', re.DOTALL)
            for m in pat.finditer(body):
                accesses.append({'type': m.group(1), 'register': m.group(
                    2), 'text': m.group(0), 'start': m.start()})
        return accesses

    def _find_delays(self, body: str) -> List[Dict[str, Any]]:
        '''
        Find all delay/timing related calls in the function body.
        '''
        delay_calls = [
            'msleep', 'udelay', 'mdelay', 'ndelay', 'usleep_range', 'msleep_interruptible',
            'schedule_timeout', 'wait_event', 'wait_for_completion', 'ssleep', 'cpu_relax'
        ]
        pat = re.compile(r'\b(' + '|'.join(delay_calls) +
                         r')\s*\((.*?)\)', re.DOTALL)
        delays = []
        for m in pat.finditer(body):
            delays.append(
                {'call': m.group(1), 'args': m.group(2), 'start': m.start()})
        return delays
