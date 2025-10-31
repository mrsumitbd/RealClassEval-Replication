
import re
import pathlib
from typing import Dict, Any, Optional, List


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
        self._function_patterns = {}  # reg_name -> re.Pattern
        self._macro_patterns = {}     # reg_name -> re.Pattern

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        '''Get cached function pattern for register name.'''
        if reg_name not in self._function_patterns:
            # Match function definitions that use reg_name inside their body
            # Function: return_type func_name(args) { ... reg_name ... }
            # We'll match the function header and body, and check for reg_name inside
            # This pattern matches function headers (with possible multiline args)
            pattern = re.compile(
                r'([a-zA-Z_][\w\s\*\(\),]*?)\s+([a-zA-Z_]\w*)\s*\(([^)]*)\)\s*\{',
                re.MULTILINE
            )
            self._function_patterns[reg_name] = pattern
        return self._function_patterns[reg_name]

    def _get_macro_pattern(self, reg_name: str) -> re.Pattern:
        '''Get cached macro pattern for register name (for split-across-lines macros).'''
        if reg_name not in self._macro_patterns:
            # Match macro invocations that use reg_name, possibly split across lines
            # e.g. MACRO_NAME(\n ... reg_name ...)
            pattern = re.compile(
                r'([A-Z_][A-Z0-9_]*\s*\([^)]*' +
                re.escape(reg_name) + r'[^)]*\))',
                re.MULTILINE | re.DOTALL
            )
            self._macro_patterns[reg_name] = pattern
        return self._macro_patterns[reg_name]

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        '''
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        '''
        results = []
        for path, content in self.file_contents.items():
            # Find all function definitions
            func_pattern = self._get_function_pattern(reg_name)
            for match in func_pattern.finditer(content):
                func_header = match.group(0)
                func_name = match.group(2)
                start = match.end()
                # Extract function body using brace balancing
                body, end_pos = self._extract_brace_block(content, start - 1)
                if reg_name in body:
                    timing = self._determine_timing(func_name, body)
                    access_pattern = self._analyze_access_pattern(
                        body, reg_name)
                    results.append({
                        'file': str(path),
                        'function': func_name,
                        'timing': timing,
                        'access_pattern': access_pattern,
                        'body': body
                    })
            # Also check for macro invocations using reg_name
            macro_pattern = self._get_macro_pattern(reg_name)
            for macro_match in macro_pattern.finditer(content):
                macro_invocation = macro_match.group(0)
                # Try to find the function this macro is in
                func_name, func_body = self._find_enclosing_function(
                    content, macro_match.start())
                timing = self._determine_timing(
                    func_name, func_body) if func_name else 'unknown'
                access_pattern = self._analyze_access_pattern(
                    func_body, reg_name) if func_body else 'unknown'
                results.append({
                    'file': str(path),
                    'function': func_name or 'macro',
                    'timing': timing,
                    'access_pattern': access_pattern,
                    'macro_invocation': macro_invocation
                })
        return {'register': reg_name, 'contexts': results}

    def _determine_timing(self, func_name: str, func_body: str) -> str:
        '''
        Determine timing context with fallback detection.
        Args:
            func_name: Name of the function
            func_body: Content of the function
        Returns:
            Timing classification string
        '''
        # Heuristics: look for keywords in function name or body
        timing_keywords = {
            'init': 'initialization',
            'probe': 'initialization',
            'setup': 'initialization',
            'reset': 'initialization',
            'irq': 'interrupt',
            'isr': 'interrupt',
            'interrupt': 'interrupt',
            'thread': 'threaded',
            'work': 'threaded',
            'poll': 'polling',
            'timer': 'timer',
            'delay': 'delayed',
            'sleep': 'delayed',
            'wait': 'delayed',
            'deinit': 'deinitialization',
            'exit': 'deinitialization',
            'remove': 'deinitialization',
        }
        func_name_lower = (func_name or '').lower()
        for key, val in timing_keywords.items():
            if key in func_name_lower:
                return val
        # Fallback: look for timing-related calls in body
        if re.search(r'\b(msleep|udelay|mdelay|usleep_range|schedule_timeout|wait_event)\b', func_body):
            return 'delayed'
        if re.search(r'\b(enable_irq|disable_irq|request_irq|free_irq)\b', func_body):
            return 'interrupt'
        if re.search(r'\bthread|kthread|workqueue|queue_work\b', func_body):
            return 'threaded'
        if re.search(r'\binit|setup|probe\b', func_body):
            return 'initialization'
        if re.search(r'\bremove|exit|deinit\b', func_body):
            return 'deinitialization'
        return 'unknown'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        '''Analyze register access patterns within a function.'''
        # Look for read/write patterns
        # e.g. reg_name = ..., ... = reg_name, or macro(reg_name, ...)
        write_pat = re.compile(r'\b' + re.escape(reg_name) + r'\s*=')
        read_pat = re.compile(r'=\s*' + re.escape(reg_name) + r'\b')
        macro_write_pat = re.compile(
            r'\b(SET|WRITE|UPDATE|MODIFY)_[A-Z0-9_]*\s*\(\s*' + re.escape(reg_name))
        macro_read_pat = re.compile(
            r'\b(GET|READ)_[A-Z0-9_]*\s*\(\s*' + re.escape(reg_name))
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
            func_pattern = re.compile(
                r'([a-zA-Z_][\w\s\*\(\),]*?)\s+([a-zA-Z_]\w*)\s*\(([^)]*)\)\s*\{',
                re.MULTILINE
            )
            for match in func_pattern.finditer(content):
                func_name = match.group(2)
                start = match.end()
                func_body, end_pos = self._extract_brace_block(
                    content, start - 1)
                accesses = []
                # Find all register accesses (optionally filter by reg_name)
                reg_pat = re.compile(r'\b([A-Z_][A-Z0-9_]*)\b')
                for reg_match in reg_pat.finditer(func_body):
                    reg = reg_match.group(1)
                    if reg_name and reg != reg_name:
                        continue
                    # Check if this is an access (read/write)
                    context = func_body[max(
                        0, reg_match.start()-20):reg_match.end()+20]
                    if re.search(r'\b' + re.escape(reg) + r'\s*=', context) or re.search(r'=\s*' + re.escape(reg) + r'\b', context):
                        accesses.append(
                            {'register': reg, 'pos': reg_match.start()})
                if accesses:
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
        delay_calls = [
            'msleep', 'udelay', 'mdelay', 'usleep_range', 'schedule_timeout',
            'wait_event', 'msleep_interruptible', 'ssleep', 'cpu_relax'
        ]
        delay_pat = re.compile(
            r'\b(' + '|'.join(delay_calls) + r')\s*\(([^)]*)\)')
        for path, content in self.file_contents.items():
            func_pattern = re.compile(
                r'([a-zA-Z_][\w\s\*\(\),]*?)\s+([a-zA-Z_]\w*)\s*\(([^)]*)\)\s*\{',
                re.MULTILINE
            )
            for match in func_pattern.finditer(content):
                func_name = match.group(2)
                start = match.end()
                func_body, end_pos = self._extract_brace_block(
                    content, start - 1)
                # If reg_name is given, only consider functions that access it
                if reg_name and reg_name not in func_body:
                    continue
                for delay_match in delay_pat.finditer(func_body):
                    delay_func = delay_match.group(1)
                    delay_arg = delay_match.group(2)
                    # Find the closest register access before this delay
                    reg_access_pat = re.compile(
                        r'\b' + re.escape(reg_name) + r'\b') if reg_name else re.compile(r'\b([A-Z_][A-Z0-9_]*)\b')
                    accesses = []
                    for reg_match in reg_access_pat.finditer(func_body[:delay_match.start()]):
                        accesses.append({'register': reg_match.group(
                            1) if not reg_name else reg_name, 'pos': reg_match.start()})
                    if accesses:
                        last_access = accesses[-1]
                    else:
                        last_access = None
                    results.append({
                        'file': str(path),
                        'function': func_name,
                        'delay_function': delay_func,
                        'delay_argument': delay_arg,
                        'preceding_access': last_access,
                        'body': func_body
                    })
        return results

    def _extract_brace_block(self, text: str, start_pos: int) -> (str, int):
        '''Extracts a block of code enclosed in braces starting at start_pos.'''
        # start_pos should be at the opening '{'
        if text[start_pos] != '{':
            # Find the next '{'
            start_pos = text.find('{', start_pos)
            if start_pos == -1:
                return '', start_pos
        brace_count = 0
        end_pos = start_pos
        for i in range(start_pos, len(text)):
            if text[i] == '{':
                brace_count += 1
            elif text[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_pos = i
                    break
        return text[start_pos+1:end_pos], end_pos+1

    def _find_enclosing_function(self, content: str, pos: int) -> (Optional[str], Optional[str]):
        '''Find the function name and body enclosing the given position.'''
        # Find all function headers before pos
        func_pattern = re.compile(
            r'([a-zA-Z_][\w\s\*\(\),]*?)\s+([a-zA-Z_]\w*)\s*\(([^)]*)\)\s*\{',
            re.MULTILINE
        )
        last_func = None
        last_func_start = None
        for match in func_pattern.finditer(content):
            if match.start() > pos:
                break
            last_func = match.group(2)
            last_func_start = match.end()
        if last_func and last_func_start is not None:
            func_body, end_pos = self._extract_brace_block(
                content, last_func_start - 1)
            if last_func_start - 1 <= pos <= end_pos:
                return last_func, func_body
        return None, None
