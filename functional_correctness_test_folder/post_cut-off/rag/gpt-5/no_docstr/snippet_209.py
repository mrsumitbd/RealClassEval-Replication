import re
import pathlib
from typing import Any, Dict, List, Optional, Tuple, Iterable


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
        self.file_contents: Dict[pathlib.Path, str] = {}
        self._normalized_contents: Dict[pathlib.Path, str] = {}
        self._function_pattern_cache: Dict[str, re.Pattern] = {}
        self._delay_re = re.compile(
            r'\b(?:udelay|mdelay|ndelay|usleep_range|usleep|fsleep|msleep(?:_interruptible)?|nanosleep)\s*\(',
            re.IGNORECASE,
        )
        self._read_call_name_re = re.compile(
            r'\b(?:ioread\d+|read[bwlq]|read(?:_relaxed)?|REG_(?:READ|GET)|READ(?:_REG)?)\b',
            re.IGNORECASE,
        )
        self._write_call_name_re = re.compile(
            r'\b(?:iowrite\d+|write[bwlq]|write(?:_relaxed)?|REG_(?:WRITE|SET|CLR|UPDATE)|WRITE(?:_REG)?)\b',
            re.IGNORECASE,
        )
        self._call_with_args_re = re.compile(
            r'(?P<name>\b\w+\b)\s*\((?P<args>.*?)\)', re.DOTALL)
        self._upper_ident_re = re.compile(r'\b[A-Z][A-Z0-9_]{2,}\b')
        self._brace_start_re = re.compile(
            r'(?m)^\s*(?:static\s+|inline\s+|static\s+inline\s+|__always_inline\s+|__maybe_unused\s+|__init\s+|__irq\s+|__attribute__\s*\(\([^)]+\)\)\s+)*'
            r'(?:[\w\*\s]+?\s+)?(?P<func_name>\w+)\s*\((?P<params>[^;{}()]*(?:\([^)]*\)[^;{}()]*)*)\)\s*\{'
        )
        for p, content in file_contents.items():
            self.file_contents[p] = content
            self._normalized_contents[p] = self._normalize_content(content)

    def _normalize_content(self, s: str) -> str:
        # Normalize line endings and join line continuations
        s = s.replace('\r\n', '\n').replace('\r', '\n')
        s = re.sub(r'\\\n', '', s)
        return s

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        '''Get cached function pattern for register name.'''
        # Keyed by reg_name to respect interface; same pattern is reused
        if reg_name not in self._function_pattern_cache:
            self._function_pattern_cache[reg_name] = self._brace_start_re
        return self._function_pattern_cache[reg_name]

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        '''
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        '''
        results: List[Dict[str, Any]] = []
        usage_token_re = re.compile(
            rf'\b{re.escape(reg_name)}\b', re.IGNORECASE | re.DOTALL)
        for path, content in self._normalized_contents.items():
            for func_name, func_body, body_start in self._iter_functions(content):
                if not usage_token_re.search(func_body):
                    # Also attempt to detect macro calls that might include the register name indirectly
                    if not self._matches_reg_in_calls(func_body, reg_name):
                        continue
                timing = self._determine_timing(func_name, func_body)
                access = self._analyze_access_pattern(func_body, reg_name)
                occurrences = len(list(usage_token_re.finditer(func_body)))
                lines: List[int] = []
                for m in usage_token_re.finditer(func_body):
                    lines.append(self._offset_to_line(
                        content, body_start + m.start()))
                result = {
                    'file': str(path),
                    'function': func_name,
                    'occurrences': occurrences,
                    'timing': timing,
                    'access': access,
                    'lines': lines,
                }
                results.append(result)
        return {'register': reg_name, 'functions': results}

    def _determine_timing(self, func_name: str, func_body: str) -> str:
        '''
        Determine timing context with fallback detection.
        Args:
            func_name: Name of the function
            func_body: Content of the function
        Returns:
            Timing classification string
        '''
        name = func_name.lower()
        body = func_body

        # Strong indicators
        if re.search(r'\b(?:irq|isr|interrupt)\b', name):
            return 'interrupt'
        if re.search(r'\brequest_irq\b', body):
            return 'interrupt'
        if re.search(r'\b(?:probe|attach|init)\b', name):
            return 'init/probe'
        if re.search(r'\b(?:suspend|resume|pm|power)\b', name) or re.search(r'\b(?:pm_runtime|suspend|resume)\b', body):
            return 'power-management'
        if re.search(r'\b(?:ioctl|read|write|open|release)\b', name):
            return 'io-path'
        if re.search(r'\b(?:napi|rx|tx)\b', name):
            return 'data-path'
        if re.search(r'\b(?:tasklet|workqueue|schedule_work|queue_work|queue_delayed_work|timer_setup|hrtimer)\b', body):
            return 'deferred'
        if self._delay_re.search(body):
            return 'delay-in-function'

        # Fallback signals
        if re.search(r'\bspin_lock_irqsave\b', body):
            return 'interrupt-sensitive'
        if re.search(r'\b(?:kthread|worker|work_struct)\b', body):
            return 'threaded/deferred'
        return 'unspecified'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        '''Analyze register access patterns within a function.'''
        write_calls = list(self._iter_calls_for_reg(
            func_body, reg_name, is_write=True))
        read_calls = list(self._iter_calls_for_reg(
            func_body, reg_name, is_write=False))

        writes = len(write_calls)
        reads = len(read_calls)

        # Detect RMW: read then modify then write (with |=, &= ~, ^=)
        rmw = False
        bit_op = None
        if reads and writes:
            first_read_pos = read_calls[0][2]
            last_write_pos = write_calls[-1][2]
            if last_write_pos > first_read_pos:
                middle = func_body[first_read_pos:last_write_pos]
                if re.search(r'\|\=|=\s*[^;]*\|\s*[^;]*;', middle):
                    rmw = True
                    bit_op = 'bit-set'
                elif re.search(r'&=\s*~|=\s*[^;]*&\s*~[^;]*;', middle):
                    rmw = True
                    bit_op = 'bit-clear'
                elif re.search(r'\^=|=\s*[^;]*\^\s*[^;]*;', middle):
                    rmw = True
                    bit_op = 'toggle'

        if rmw:
            return f'read-modify-write{f" ({bit_op})" if bit_op else ""}'
        if writes > 1 and not reads:
            return 'multi-write'
        if reads > 1 and not writes:
            return 'multi-read'
        if writes and not reads:
            return 'write-only'
        if reads and not writes:
            return 'read-only'
        if reads and writes:
            return 'read-and-write'
        return 'unknown'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''
        Analyze register access sequences with improved function parsing.
        Enhanced to handle nested braces properly using balance counter.
        '''
        results: List[Dict[str, Any]] = []
        for path, content in self._normalized_contents.items():
            for func_name, func_body, body_start in self._iter_functions(content):
                events = []  # (pos, kind, dict)
                # Collect read/write events
                for m in self._call_with_args_re.finditer(func_body):
                    name = m.group('name')
                    args = m.group('args')
                    pos = m.start()
                    kind: Optional[str] = None
                    if self._write_call_name_re.search(name):
                        kind = 'write'
                    elif self._read_call_name_re.search(name):
                        kind = 'read'
                    elif self._delay_re.search(name):
                        kind = 'delay'
                    else:
                        # detect delay calls via args scanning (rare but keep)
                        if self._delay_re.search(name + '('):
                            kind = 'delay'

                    if not kind:
                        continue

                    reg_in_call = self._extract_register_from_args(
                        args, fallback=None)
                    if reg_name is not None:
                        # keep only calls referencing the requested register
                        if kind != 'delay' and not self._reg_matches(reg_in_call, reg_name, args):
                            continue

                    line = self._offset_to_line(content, body_start + pos)
                    events.append(
                        (pos, kind, {'call': name, 'args': args, 'line': line, 'register': reg_in_call}))

                # Add standalone delay events not captured as function calls in the previous loop
                for d in self._delay_re.finditer(func_body):
                    pos = d.start()
                    line = self._offset_to_line(content, body_start + pos)
                    events.append((pos, 'delay', {'call': d.group(0).split(
                        '(')[0], 'args': '', 'line': line, 'register': None}))
                events.sort(key=lambda x: x[0])

                if not events:
                    continue

                sequence = []
                has_delay = any(kind == 'delay' for _, kind, _ in events)
                for _, kind, detail in events:
                    if reg_name is not None and kind != 'delay':
                        # Only keep entries for requested register
                        if not self._reg_matches(detail.get('register'), reg_name, detail.get('args', '')):
                            continue
                    sequence.append({'op': kind, **detail})

                if not sequence:
                    continue

                timing = self._determine_timing(func_name, func_body)
                results.append({
                    'file': str(path),
                    'function': func_name,
                    'timing': timing,
                    'has_delay': has_delay,
                    'register': reg_name,
                    'sequence': sequence,
                })
        return results

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''Analyze timing constraints and delays related to register accesses.'''
        constraints: List[Dict[str, Any]] = []
        window_chars = 200  # proximity window for delay-after-access
        for path, content in self._normalized_contents.items():
            for func_name, func_body, body_start in self._iter_functions(content):
                # Collect access and delay positions
                # (pos, kind, call, args)
                access_matches: List[Tuple[int, str, str, str]] = []
                for m in self._call_with_args_re.finditer(func_body):
                    name = m.group('name')
                    args = m.group('args')
                    pos = m.start()
                    if self._write_call_name_re.search(name):
                        kind = 'write'
                    elif self._read_call_name_re.search(name):
                        kind = 'read'
                    else:
                        continue
                    if reg_name is not None:
                        reg_in_call = self._extract_register_from_args(
                            args, fallback=None)
                        if not self._reg_matches(reg_in_call, reg_name, args):
                            continue
                    access_matches.append((pos, kind, name, args))

                delay_matches = list(self._delay_re.finditer(func_body))
                if not access_matches or not delay_matches:
                    continue

                for pos, kind, call, args in access_matches:
                    # Find nearest following delay in window or before next access
                    next_access_pos = min(
                        (p for p, _, _, _ in access_matches if p > pos), default=len(func_body))
                    # Check delays within window and before next access
                    for dm in delay_matches:
                        dpos = dm.start()
                        if pos <= dpos <= min(next_access_pos, pos + window_chars):
                            line_access = self._offset_to_line(
                                content, body_start + pos)
                            line_delay = self._offset_to_line(
                                content, body_start + dpos)
                            delay_call = dm.group(0).split('(')[0]
                            constraints.append({
                                'file': str(path),
                                'function': func_name,
                                'op': kind,
                                'access_call': call,
                                'access_line': line_access,
                                'delay_call': delay_call,
                                'delay_line': line_delay,
                                'register': self._extract_register_from_args(args, fallback=reg_name),
                                'timing': self._determine_timing(func_name, func_body),
                            })
                            break  # one delay association per access is enough
        return constraints

    # Internal helpers

    def _matches_reg_in_calls(self, func_body: str, reg_name: str) -> bool:
        # Check if any call arguments contain the register name across lines
        reg_token = re.compile(rf'\b{re.escape(reg_name)}\b', re.IGNORECASE)
        for m in self._call_with_args_re.finditer(func_body):
            if reg_token.search(m.group('args')):
                return True
        return False

    def _iter_calls_for_reg(self, func_body: str, reg_name: str, is_write: bool) -> Iterable[Tuple[str, str, int]]:
        name_re = self._write_call_name_re if is_write else self._read_call_name_re
        reg_token = re.compile(rf'\b{re.escape(reg_name)}\b', re.IGNORECASE)
        for m in self._call_with_args_re.finditer(func_body):
            name = m.group('name')
            if not name_re.search(name):
                continue
            args = m.group('args')
            if reg_token.search(args):
                yield (name, args, m.start())

    def _extract_register_from_args(self, args: str, fallback: Optional[str]) -> Optional[str]:
        # Attempt to extract uppercase-like identifiers (typical register macro names)
        # Prefer the first argument token that looks like a register macro
        # Split by comma to bias toward first argument
        parts = [p for p in re.split(r'\s*,\s*', args) if p]
        for p in parts:
            m = self._upper_ident_re.search(p)
            if m:
                return m.group(0)
        # If none, search the entire args
        m = self._upper_ident_re.search(args)
        if m:
            return m.group(0)
        return fallback

    def _reg_matches(self, extracted: Optional[str], target: str, args: str) -> bool:
        if extracted and extracted.lower() == target.lower():
            return True
        return re.search(rf'\b{re.escape(target)}\b', args, re.IGNORECASE) is not None

    def _offset_to_line(self, content: str, offset: int) -> int:
        # Compute 1-based line number from absolute offset
        return content.count('\n', 0, max(0, offset)) + 1

    def _iter_functions(self, content: str) -> Iterable[Tuple[str, str, int]]:
        # Iterate function definitions by locating the signature and then matching braces
        for m in self._brace_start_re.finditer(content):
            func_name = m.group('func_name')
            brace_open_pos = content.find('{', m.end() - 1)
            if brace_open_pos == -1:
                continue
            brace_close_pos = self._find_matching_brace(
                content, brace_open_pos)
            if brace_close_pos == -1:
                continue
            body = content[brace_open_pos + 1:brace_close_pos]
            yield func_name, body, brace_open_pos + 1

    def _find_matching_brace(self, s: str, open_pos: int) -> int:
        depth = 0
        i = open_pos
        n = len(s)
        in_squote = False
        in_dquote = False
        in_line_comment = False
        in_block_comment = False
        while i < n:
            ch = s[i]
            nxt = s[i+1] if i + 1 < n else ''
            if in_line_comment:
                if ch == '\n':
                    in_line_comment = False
                i += 1
                continue
            if in_block_comment:
                if ch == '*' and nxt == '/':
                    in_block_comment = False
                    i += 2
                else:
                    i += 1
                continue
            if in_squote:
                if ch == '\\':
                    i += 2
                    continue
                if ch == "'":
                    in_squote = False
                i += 1
                continue
            if in_dquote:
                if ch == '\\':
                    i += 2
                    continue
                if ch == '"':
                    in_dquote = False
                i += 1
                continue

            if ch == '/' and nxt == '/':
                in_line_comment = True
                i += 2
                continue
            if ch == '/' and nxt == '*':
                in_block_comment = True
                i += 2
                continue
            if ch == "'":
                in_squote = True
                i += 1
                continue
            if ch == '"':
                in_dquote = True
                i += 1
                continue

            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return i
            i += 1
        return -1
