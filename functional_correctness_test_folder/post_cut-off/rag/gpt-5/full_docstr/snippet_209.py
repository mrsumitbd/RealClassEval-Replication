import re
import pathlib
from typing import Any, Dict, List, Optional, Tuple


class DriverAnalyzer:
    '''
    Encapsulates driver analysis functionality with shared state.
    This class maintains pre-compiled regex patterns and file content
    to avoid duplication and improve performance.
    '''

    # Common patterns for register accesses and timing
    _WRITE_FUNCS = (
        r'\bwritel(?:_relaxed)?\b',
        r'\bwriteb\b',
        r'\bwritew\b',
        r'\bwriteq\b',
        r'\bregmap_write\b',
        r'\bSETBITS?_?(?:LE|BE)?\b',
        r'\bCLRBITS?_?(?:LE|BE)?\b',
        r'\bCLRSETBITS?_?(?:LE|BE)?\b',
        r'\bWRITE\w*\b',  # generic macro
        r'\bset_bits?\b',
        r'\bclear_bits?\b',
        r'\bupdate_bits?\b',
    )
    _READ_FUNCS = (
        r'\breadl(?:_relaxed)?\b',
        r'\breadb\b',
        r'\breadw\b',
        r'\breadq\b',
        r'\bregmap_read\b',
        r'\bREAD\w*\b',  # generic macro
        r'\bget_bits?\b',
    )
    _DELAY_FUNCS = (
        r'\budelay\b',
        r'\bndelay\b',
        r'\bmdelay\b',
        r'\busleep(?:_range)?\b',
        r'\bmsleep(?:_interruptible|_range)?\b',
        r'\bschedule_timeout(?:_interruptible)?\b',
        r'\bschedule\b',
        r'\bhrtimer_(?:start|sleep|get_remaining)\b',
        r'\bread[qlbw]_poll_timeout\b',
        r'\breadx_poll_timeout\b',
        r'\bwait_for_completion(?:_timeout)?\b',
    )

    def __init__(self, file_contents: Dict[pathlib.Path, str]):
        '''
        Initialize analyzer with file contents.
        Args:
            file_contents: Dictionary mapping file paths to their content
        '''
        self.file_contents: Dict[pathlib.Path, str] = file_contents
        self._usage_pattern_cache: Dict[str, re.Pattern] = {}
        self._func_headers_re = re.compile(
            r'''
            (?P<prefix>^|[;{}\n])                                   # start or boundary
            (?P<signature>                                           # whole signature (no body)
                (?:[A-Za-z_][\w\s\*\(\)\[\],\.]+?\s+)?               # return type and qualifiers
                (?P<name>[A-Za-z_]\w*)\s*                            # function name
                \(
                    (?:[^(){};]|\([^()]*\))*                         # args (naively balanced parens)
                \)\s*
            )
            \{                                                       # opening brace of function body
            ''',
            re.MULTILINE | re.VERBOSE,
        )
        # Pre-compiled regexes for reads/writes/delays
        self._write_re = re.compile('|'.join(self._WRITE_FUNCS))
        self._read_re = re.compile('|'.join(self._READ_FUNCS))
        self._delay_re = re.compile('|'.join(self._DELAY_FUNCS))
        self._call_name_re = re.compile(r'\b([A-Za-z_]\w*)\s*\(')
        self._macro_call_name_re = re.compile(r'\b([A-Z][A-Z0-9_]{2,})\s*\(')
        self._uppercase_token_re = re.compile(r'\b([A-Z][A-Z0-9_]{2,})\b')

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        '''Get cached function pattern for register name.'''
        if reg_name not in self._usage_pattern_cache:
            # Match register usage possibly inside macros split across lines.
            # We allow arbitrary whitespace around tokens and across lines.
            # We also try to capture common read/write macro names around the reg.
            escaped = re.escape(reg_name)
            usage = rf'\b{escaped}\b'
            macro_context = rf'(?:{ "|".join([p[2:-2] for p in self._WRITE_FUNCS + self._READ_FUNCS]) })'
            pattern = rf'(?s)(?:{macro_context}\s*\([^)]*?{usage}[^)]*\)|{usage})'
            self._usage_pattern_cache[reg_name] = re.compile(
                pattern, re.MULTILINE)
        return self._usage_pattern_cache[reg_name]

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        '''
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        '''
        results: List[Dict[str, Any]] = []
        usage_pat = self._get_function_pattern(reg_name)

        for path, text in self.file_contents.items():
            for func_name, func_body, header_span, body_span in self._iter_functions(text):
                body = func_body
                if usage_pat.search(body):
                    timing = self._determine_timing(func_name, body)
                    access = self._analyze_access_pattern(body, reg_name)
                    calls = self._collect_calls(body)
                    macros = self._collect_macros(body)
                    usage_lines = self._collect_usage_context(
                        text, body_span, reg_name)

                    results.append({
                        'file': str(path),
                        'function': func_name,
                        'timing': timing,
                        'access_pattern': access,
                        'calls': calls,
                        'macros': macros,
                        'usage_context': usage_lines,
                    })
        return {
            'reg_name': reg_name,
            'occurrences': results,
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
        name_l = func_name.lower()
        body = func_body

        if re.search(r'\b(irq_handler_t|irqreturn_t|request_irq|free_irq|IRQF_)', body) or re.search(r'\birq\b', name_l):
            return 'interrupt-context'
        if re.search(r'\b(tasklet|work_struct|INIT_WORK|schedule_work|queue_work|delayed_work|timer_list|hrtimer_)\b', body):
            return 'deferred/bottom-half'
        if re.search(r'\b(init|probe|setup|attach|bringup)\b', name_l):
            return 'init/probe'
        if self._delay_re.search(body) or re.search(r'\bschedule\(', body):
            return 'process-context'
        if re.search(r'\bspin_lock(?:_irqsave|_bh)?\b', body) and not self._delay_re.search(body):
            return 'atomic'
        if re.search(r'\b(mutex_lock|down|sema|rwsem)\b', body):
            return 'process-context'

        # Fallback timing detection heuristics
        if re.search(r'\b(for|while)\s*\(', body) and re.search(r'\b(timeout|delay|deadline|jiffies)\b', body):
            return 'polling-with-timeout'
        return 'unknown'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        '''Analyze register access patterns within a function.'''
        reads: List[Tuple[int, str]] = []
        writes: List[Tuple[int, str]] = []
        delays_present = bool(self._delay_re.search(func_body))

        for lineno, line in self._iter_lines(func_body):
            if reg_name not in line:
                continue
            if self._write_re.search(line):
                writes.append((lineno, line.strip()))
            if self._read_re.search(line):
                reads.append((lineno, line.strip()))

        if not reads and not writes:
            # Could be macro without read/write keywords, fallback: detect assignment
            assign_lines = [(ln, l.strip()) for ln, l in self._iter_lines(
                func_body) if reg_name in l and ('=' in l or '|' in l or '&' in l)]
            if assign_lines:
                writes = assign_lines

        if reads and writes:
            pattern = 'read-modify-write' if self._is_rmw_sequence(
                reads, writes) else 'read-and-write'
        elif writes and len(writes) > 1:
            pattern = 'multiple-writes'
        elif writes:
            pattern = 'write-only'
        elif reads:
            pattern = 'read-only'
        else:
            pattern = 'unknown'

        if delays_present:
            pattern += '+delay'
        return pattern

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''
        Analyze register access sequences with improved function parsing.
        Enhanced to handle nested braces properly using balance counter.
        '''
        sequences: List[Dict[str, Any]] = []

        for path, text in self.file_contents.items():
            for func_name, func_body, _, _ in self._iter_functions(text):
                events: List[Dict[str, Any]] = []
                for lineno, line in self._iter_lines(func_body):
                    line_stripped = line.strip()

                    # Detect writes and reads
                    write_m = self._write_re.search(line_stripped)
                    read_m = self._read_re.search(line_stripped)

                    if not write_m and not read_m:
                        continue

                    # Extract candidate register names (uppercase tokens)
                    regs = set(self._uppercase_token_re.findall(line_stripped))
                    # Filter to target reg_name if provided
                    if reg_name is not None and reg_name not in regs and reg_name not in line_stripped:
                        continue

                    op = 'write' if write_m and not read_m else (
                        'read' if read_m and not write_m else 'read/write')
                    # Try to grab call name and args
                    call_name = None
                    call_match = self._call_name_re.search(line_stripped)
                    if call_match:
                        call_name = call_match.group(1)

                    events.append({
                        'line': lineno,
                        'op': op,
                        'call': call_name,
                        'registers': sorted(regs) if regs else ([reg_name] if reg_name else []),
                        'text': line_stripped,
                    })

                if events:
                    sequences.append({
                        'file': str(path),
                        'function': func_name,
                        'sequence': events,
                        'counts': {
                            'reads': sum(1 for e in events if e['op'] == 'read'),
                            'writes': sum(1 for e in events if e['op'] == 'write'),
                            'ambiguous': sum(1 for e in events if e['op'] == 'read/write'),
                        }
                    })

        return sequences

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''Analyze timing constraints and delays related to register accesses.'''
        reports: List[Dict[str, Any]] = []

        for path, text in self.file_contents.items():
            for func_name, func_body, _, _ in self._iter_functions(text):
                if reg_name is not None and not self._get_function_pattern(reg_name).search(func_body):
                    continue

                timing_calls: List[Dict[str, Any]] = []
                classification = 'none'

                for lineno, line in self._iter_lines(func_body):
                    if (m := self._delay_re.search(line)):
                        call_name = m.group(0)
                        args = self._extract_args_after_call(line, call_name)
                        timing_calls.append(
                            {'line': lineno, 'name': call_name, 'args': args, 'text': line.strip()})

                if timing_calls:
                    # Classify based on call types
                    if any(re.search(r'\b(msleep|mdelay|schedule)', c['name']) for c in timing_calls):
                        classification = 'sleep/blocking'
                    elif any(re.search(r'\b(udelay|ndelay|poll_timeout)', c['name']) for c in timing_calls):
                        classification = 'busy-wait/poll'
                    else:
                        classification = 'timing-calls-present'
                else:
                    # Fallback: detect polling with timeout loops
                    if self._detect_polling_timeout(func_body):
                        classification = 'polling-with-timeout'

                if timing_calls or classification != 'none':
                    reports.append({
                        'file': str(path),
                        'function': func_name,
                        'classification': classification,
                        'timing_calls': timing_calls,
                    })

        return reports

    # ---------------- Internal helpers ----------------

    def _iter_functions(self, text: str) -> List[Tuple[str, str, Tuple[int, int], Tuple[int, int]]]:
        results: List[Tuple[str, str, Tuple[int, int], Tuple[int, int]]] = []
        for m in self._func_headers_re.finditer(text):
            name = m.group('name')
            header_start = m.start('signature')
            body_start = m.end()  # right after '{'
            body_end = self._find_matching_brace(
                text, body_start - 1)  # pass index of '{'
            if body_end is None:
                continue
            body = text[body_start:body_end]
            results.append((name, body, (m.start('signature'),
                           m.end('signature')), (body_start, body_end)))
        return results

    def _find_matching_brace(self, text: str, opening_index: int) -> Optional[int]:
        # 'opening_index' points to '{'
        if opening_index < 0 or opening_index >= len(text) or text[opening_index] != '{':
            return None
        depth = 0
        i = opening_index
        in_char = False
        in_str = False
        escape = False
        while i < len(text):
            ch = text[i]
            if in_str:
                if escape:
                    escape = False
                elif ch == '\\':
                    escape = True
                elif ch == '"':
                    in_str = False
            elif in_char:
                if escape:
                    escape = False
                elif ch == '\\':
                    escape = True
                elif ch == "'":
                    in_char = False
            else:
                if ch == '"':
                    in_str = True
                elif ch == "'":
                    in_char = True
                elif ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth == 0:
                        return i
            i += 1
        return None

    def _collect_calls(self, func_body: str) -> List[str]:
        calls = []
        for m in self._call_name_re.finditer(func_body):
            name = m.group(1)
            if name in ('if', 'for', 'while', 'switch', 'return', 'sizeof'):
                continue
            calls.append(name)
        # Deduplicate preserving order
        seen = set()
        uniq = []
        for c in calls:
            if c not in seen:
                uniq.append(c)
                seen.add(c)
        return uniq

    def _collect_macros(self, func_body: str) -> List[str]:
        macros = []
        for m in self._macro_call_name_re.finditer(func_body):
            macros.append(m.group(1))
        seen = set()
        uniq = []
        for c in macros:
            if c not in seen:
                uniq.append(c)
                seen.add(c)
        return uniq

    def _collect_usage_context(self, full_text: str, body_span: Tuple[int, int], reg_name: str, context: int = 2) -> List[Dict[str, Any]]:
        start, end = body_span
        body_text = full_text[start:end]
        lines = body_text.splitlines()
        results: List[Dict[str, Any]] = []
        for idx, line in enumerate(lines, start=1):
            if reg_name in line:
                lo = max(1, idx - context)
                hi = min(len(lines), idx + context)
                results.append({
                    'line': idx,
                    'snippet': '\n'.join(lines[lo - 1:hi]),
                })
        return results

    def _iter_lines(self, text: str) -> List[Tuple[int, str]]:
        lines = text.splitlines()
        return list(enumerate(lines, start=1))

    def _is_rmw_sequence(self, reads: List[Tuple[int, str]], writes: List[Tuple[int, str]]) -> bool:
        if not reads or not writes:
            return False
        first_write_line = min(w[0] for w in writes)
        first_read_line = min(r[0] for r in reads)
        # RMW if any read occurs before a write and write line uses bitwise ops
        rmw_write = any(
            re.search(r'[\|\&\^]|CLRSET|UPDATE|MASK', w[1]) for w in writes)
        return first_read_line <= first_write_line and rmw_write

    def _extract_args_after_call(self, line: str, call_name: str) -> str:
        # naive extract: find '(' after call_name and take until ')'
        idx = line.find(call_name)
        if idx < 0:
            return ''
        idx = line.find('(', idx)
        if idx < 0:
            return ''
        depth = 0
        end = idx
        while end < len(line):
            ch = line[end]
            if ch == '(':
                depth += 1
            elif ch == ')':
                depth -= 1
                if depth == 0:
                    return line[idx + 1:end].strip()
            end += 1
        return line[idx + 1:].strip()

    def _detect_polling_timeout(self, body: str) -> bool:
        if not re.search(r'\b(for|while)\s*\(', body):
            return False
        if re.search(r'\btimeout\b', body) or re.search(r'\bjiffies\b', body) or re.search(r'\bktime\b', body):
            return True
        # polling on bit with read in loop
        if self._read_re.search(body) and re.search(r'\bwhile\s*\([^)]*\)', body):
            return True
        return False
