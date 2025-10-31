import re
import pathlib
from typing import Dict, Any, Optional, List, Tuple, Iterable


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
        self.file_contents: Dict[pathlib.Path, str] = file_contents
        self._func_pattern_cache: Dict[str, re.Pattern] = {}

        # Function header regex: capture function name and the "{" that starts the body
        # Tries to avoid control statements and declarations without body.
        self._fn_header_re = re.compile(
            r'''
            (?P<header>
                ^[ \t]*
                (?:
                    (?:static|inline|const|extern|__\w+)\s+
                )*
                (?:[A-Za-z_]\w*[\s\*]+)+      # return type (rough)
                (?P<name>[A-Za-z_]\w*)
                \s*
                \(
                    (?P<params>
                        [^;{}()]*
                        (?:\([^)]*\)[^;{}()]*)*
                    )
                \)
                \s*
            )
            \{
            ''',
            re.MULTILINE | re.DOTALL | re.VERBOSE,
        )

        # Read/Write function name sets and a combined call regex (multiline-aware)
        write_names = [
            'writel', 'writeb', 'writew', 'writeq',
            'iowrite8', 'iowrite16', 'iowrite32', 'iowrite64',
            'regmap_write',
            'REG_WRITE', 'WRITE_REG', 'SET_REG', 'WR_REG',
            'OUTB', 'OUTW', 'OUTL', 'OUTQ', 'outb', 'outw', 'outl', 'outq'
        ]
        read_names = [
            'readl', 'readb', 'readw', 'readq',
            'ioread8', 'ioread16', 'ioread32', 'ioread64',
            'regmap_read',
            'REG_READ', 'READ_REG', 'RD_REG',
            'INB', 'INW', 'INL', 'INQ', 'inb', 'inw', 'inl', 'inq'
        ]
        # Include base "read"/"write" cautiously at the end to avoid false positives
        write_names += ['write']
        read_names += ['read']

        # Build name sets for quick classification
        self._write_name_set = set(write_names)
        self._read_name_set = set(read_names)

        # Combined call regex that captures call name and its (approximate) args
        # The args group tolerates nested parentheses one level deep.
        self._call_re = re.compile(
            r'\b(?P<name>' + '|'.join(re.escape(n) for n in sorted(self._write_name_set | self._read_name_set, key=len, reverse=True)) +
            r')\s*\('
            r'(?P<args>(?:[^()]+|\([^)]*\))*)\)',
            re.MULTILINE | re.DOTALL
        )

        # Assignment statements to detect direct register assignment patterns
        self._assign_re_tpl = r'(?P<lhs>[^;=\n]{{0,120}}\b{reg}\b[^;=\n]{{0,120}})\s*=\s*(?P<rhs>[^;]*);'

        # Delay and sleep family patterns
        self._delay_specs: List[Tuple[str, re.Pattern, str]] = [
            ('udelay', re.compile(r'\budelay\s*\(\s*(?P<val>\d+)\s*\)', re.MULTILINE), 'us'),
            ('ndelay', re.compile(r'\bndelay\s*\(\s*(?P<val>\d+)\s*\)', re.MULTILINE), 'ns'),
            ('mdelay', re.compile(r'\bmdelay\s*\(\s*(?P<val>\d+)\s*\)', re.MULTILINE), 'ms'),
            ('msleep', re.compile(r'\bmsleep\s*\(\s*(?P<val>\d+)\s*\)', re.MULTILINE), 'ms'),
            ('usleep_range', re.compile(
                r'\busleep_range\s*\(\s*(?P<min>\d+)\s*,\s*(?P<max>\d+)\s*\)', re.MULTILINE), 'us'),
            ('fsleep', re.compile(r'\bfsleep\s*\(\s*(?P<val>\d+)\s*\)', re.MULTILINE), 'us'),
            ('schedule_timeout', re.compile(
                r'\bschedule_timeout\s*\(\s*(?P<val>[^)]+)\)', re.MULTILINE), 'jiffies'),
            ('msleep_interruptible', re.compile(
                r'\bmsleep_interruptible\s*\(\s*(?P<val>\d+)\s*\)', re.MULTILINE), 'ms'),
        ]

        # Common markers for masked/bit operations
        self._mask_near_re = re.compile(
            r'\b(?:MASK|_MASK|BITS?|BIT\(|SHIFT|_SHIFT)\b')

        # Comment patterns for timing clues
        self._timing_comment_re = re.compile(r'//.*|/\*.*?\*/', re.DOTALL)

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        '''Get cached function pattern for register name.'''
        if reg_name in self._func_pattern_cache:
            return self._func_pattern_cache[reg_name]
        # Matches any read/write macro invocation that references the register name across lines
        pat = re.compile(
            r'(?:\b(?:writel|writeb|writew|writeq|iowrite8|iowrite16|iowrite32|iowrite64|regmap_(?:read|write)|'
            r'REG_(?:READ|WRITE)|WRITE_REG|READ_REG|SET_REG|RD_REG|WR_REG|OUT[BLWQ]|IN[BLWQ]|readl|readb|readw|readq|'
            r'write|read)\s*\('
            r'(?:[^)(]+|\([^)]*\))*?\b' + re.escape(reg_name) + r'\b'
            r'(?:[^)(]+|\([^)]*\))*\))',
            re.MULTILINE | re.DOTALL
        )
        self._func_pattern_cache[reg_name] = pat
        return pat

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        '''
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        '''
        results: List[Dict[str, Any]] = []
        pat = self._get_function_pattern(reg_name)

        for path, content in self.file_contents.items():
            for fn in self._iter_functions(path, content):
                body = fn['body']
                if not pat.search(body) and (reg_name not in body):
                    continue

                timing = self._determine_timing(fn['name'], body)
                access_summary = self._analyze_access_pattern(body, reg_name)

                # Collect occurrences with cross-line macro support
                occurrences = []
                for m in pat.finditer(body):
                    occ_index = m.start()
                    line = fn['start_line'] + body[:occ_index].count('\n')
                    text = body[max(0, occ_index - 80):occ_index + 160]
                    occurrences.append({
                        'line': line + 1,
                        'snippet': text.strip()
                    })

                # Also consider simple occurrences to catch non-macro direct usages
                if not occurrences:
                    for m in re.finditer(r'\b' + re.escape(reg_name) + r'\b', body, re.MULTILINE):
                        occ_index = m.start()
                        line = fn['start_line'] + body[:occ_index].count('\n')
                        text = body[max(0, occ_index - 80):occ_index + 160]
                        occurrences.append({
                            'line': line + 1,
                            'snippet': text.strip()
                        })

                macros_spanning_lines = 0
                for occ in occurrences:
                    snip = occ['snippet']
                    if '\n' in snip and '(' in snip and ')' in snip:
                        macros_spanning_lines += 1

                results.append({
                    'file': str(fn['file']),
                    'function': fn['name'],
                    'timing': timing,
                    'access': access_summary,
                    'occurrences': len(occurrences),
                    'multi_line_macros': macros_spanning_lines,
                    'examples': occurrences[:3],  # limit examples for brevity
                })

        return {
            'register': reg_name,
            'functions': results,
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
        name_lower = func_name.lower()

        # Primary classification based on function name
        if any(k in name_lower for k in ('probe', 'init')):
            return 'init/probe'
        if any(k in name_lower for k in ('remove', 'exit', 'deinit', 'cleanup')):
            return 'remove/cleanup'
        if any(k in name_lower for k in ('suspend', 'hibernate', 'pm_suspend')):
            return 'suspend'
        if any(k in name_lower for k in ('resume', 'pm_resume', 'restore')):
            return 'resume'
        if any(k in name_lower for k in ('irq', 'isr', 'interrupt', 'hardirq', 'softirq')):
            return 'interrupt'

        # Fallback: detect context clues in signature/body
        header = func_body[:200]
        if re.search(r'\birqreturn_t\b|\bIRQ[Ff]', header):
            return 'interrupt'
        # Sleep/delay -> process context
        if any(spec[1].search(func_body) for spec in self._delay_specs):
            return 'process (sleepable)'
        # Workqueues/threads
        if re.search(r'\b(work_struct|delayed_work|kthread|workqueue)\b', func_body):
            return 'deferred (workqueue/thread)'
        # IO paths often have read/write in name
        if re.search(r'\b(read|write|io|xfer|transfer)\b', name_lower):
            return 'runtime I/O'

        return 'runtime'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        '''Analyze register access patterns within a function.'''
        reads = 0
        writes = 0
        masked = False

        # Via macro calls
        for m in self._call_re.finditer(func_body):
            call_name = m.group('name')
            args = m.group('args')
            if reg_name not in args:
                continue
            if call_name in self._write_name_set:
                writes += 1
            elif call_name in self._read_name_set:
                reads += 1
            # Check masking/bit usage nearby args
            if self._mask_near_re.search(args):
                masked = True

        # Via direct assignment patterns
        assign_re = re.compile(
            self._assign_re_tpl.format(reg=re.escape(reg_name)))
        for m in assign_re.finditer(func_body):
            writes += 1
            rhs = m.group('rhs')
            if self._mask_near_re.search(rhs):
                masked = True

        # Via usage on RHS (reads)
        use_re = re.compile(
            r'[^;]*\b' + re.escape(reg_name) + r'\b[^;]*;', re.MULTILINE)
        for m in use_re.finditer(func_body):
            stmt = m.group(0)
            if '=' in stmt:
                # If reg_name appears on RHS only, count as read
                lhs_part = stmt.split('=', 1)[0]
                if re.search(r'\b' + re.escape(reg_name) + r'\b', lhs_part):
                    # Already counted as write above
                    continue
                reads += 1
            else:
                reads += 1
            if self._mask_near_re.search(stmt):
                masked = True

        if reads and writes:
            base = 'read-write'
        elif writes:
            base = 'write'
        elif reads:
            base = 'read'
        else:
            base = 'unknown'

        if base != 'unknown' and masked:
            base += ' (masked)'
        return base

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''
        Analyze register access sequences with improved function parsing.
        Enhanced to handle nested braces properly using balance counter.
        '''
        sequences: List[Dict[str, Any]] = []

        for path, content in self.file_contents.items():
            for fn in self._iter_functions(path, content):
                events = self._extract_events(
                    fn['body'], fn['start_line'], filter_reg=reg_name)
                if not events:
                    continue

                sequences.append({
                    'file': str(fn['file']),
                    'function': fn['name'],
                    'timing': self._determine_timing(fn['name'], fn['body']),
                    'sequence': events,
                })

        return sequences

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''Analyze timing constraints and delays related to register accesses.'''
        constraints: List[Dict[str, Any]] = []

        for path, content in self.file_contents.items():
            for fn in self._iter_functions(path, content):
                body = fn['body']
                events = self._extract_events(
                    body, fn['start_line'], filter_reg=reg_name)
                if not events:
                    continue

                # Identify write-then-delay and read-after-delay patterns
                for i, ev in enumerate(events):
                    if ev['type'] in ('write', 'read'):
                        # Look ahead for a delay within a few events or lines
                        for j in range(i + 1, min(i + 6, len(events))):
                            next_ev = events[j]
                            if next_ev['type'] == 'delay':
                                # Constrain if to the same register when available
                                if reg_name is None or ev.get('register') == reg_name or next_ev.get('register') == reg_name:
                                    constraints.append({
                                        'file': str(fn['file']),
                                        'function': fn['name'],
                                        'timing': self._determine_timing(fn['name'], body),
                                        'register': ev.get('register'),
                                        'pattern': f"{ev['type']}-then-delay",
                                        'delay': {
                                            'name': next_ev.get('name'),
                                            'value': next_ev.get('value'),
                                            'unit': next_ev.get('unit'),
                                        },
                                        'lines': [ev['line'], next_ev['line']],
                                    })
                                break

                # Comments indicating timing expectations near register accesses
                for m in self._timing_comment_re.finditer(body):
                    text = m.group(0)
                    if re.search(r'\b(wait|delay|settle|stabiliz|hold|timing)\b', text, re.IGNORECASE):
                        comment_line = fn['start_line'] + \
                            body[:m.start()].count('\n') + 1
                        constraints.append({
                            'file': str(fn['file']),
                            'function': fn['name'],
                            'timing': self._determine_timing(fn['name'], body),
                            'register': reg_name,
                            'pattern': 'comment-timing-hint',
                            'details': text.strip(),
                            'lines': [comment_line],
                        })

        return constraints

    # ------------------------- internal helpers -------------------------

    def _iter_functions(self, path: pathlib.Path, content: str) -> Iterable[Dict[str, Any]]:
        for m in self._fn_header_re.finditer(content):
            name = m.group('name')
            body_start = m.end() - 1  # points at '{'
            body_end = self._find_matching_brace(content, body_start)
            if body_end is None:
                continue
            body = content[body_start + 1:body_end]  # inside braces
            start_line = content[:body_start].count('\n') + 1
            yield {
                'file': path,
                'name': name,
                'body': body,
                'start_index': body_start + 1,
                'end_index': body_end,
                'start_line': start_line,
            }

    def _find_matching_brace(self, content: str, open_brace_idx: int) -> Optional[int]:
        balance = 0
        i = open_brace_idx
        n = len(content)

        in_sl_comment = False
        in_ml_comment = False
        in_squote = False
        in_dquote = False
        escape = False

        while i < n:
            ch = content[i]

            if in_sl_comment:
                if ch == '\n':
                    in_sl_comment = False
                i += 1
                continue
            if in_ml_comment:
                if ch == '*' and i + 1 < n and content[i + 1] == '/':
                    in_ml_comment = False
                    i += 2
                else:
                    i += 1
                continue
            if in_squote:
                if not escape and ch == '\\':
                    escape = True
                elif escape:
                    escape = False
                elif ch == '\'':
                    in_squote = False
                i += 1
                continue
            if in_dquote:
                if not escape and ch == '\\':
                    escape = True
                elif escape:
                    escape = False
                elif ch == '"':
                    in_dquote = False
                i += 1
                continue

            # Not inside any special context
            if ch == '/' and i + 1 < n:
                if content[i + 1] == '/':
                    in_sl_comment = True
                    i += 2
                    continue
                if content[i + 1] == '*':
                    in_ml_comment = True
                    i += 2
                    continue
            if ch == '\'':
                in_squote = True
                i += 1
                continue
            if ch == '"':
                in_dquote = True
                i += 1
                continue

            if ch == '{':
                balance += 1
            elif ch == '}':
                balance -= 1
                if balance == 0:
                    return i
            i += 1

        return None

    def _extract_events(self, func_body: str, func_start_line: int, *, filter_reg: Optional[str] = None) -> List[Dict[str, Any]]:
        events: List[Dict[str, Any]] = []

        # Find delays
        for name, rx, unit in self._delay_specs:
            for m in rx.finditer(func_body):
                start = m.start()
                line = func_start_line + func_body[:start].count('\n') + 1
                ev: Dict[str, Any] = {
                    'type': 'delay', 'name': name, 'line': line, 'index': start, 'unit': unit}
                if name == 'usleep_range':
                    ev['value'] = (int(m.group('min')), int(m.group('max')))
                else:
                    val = m.groupdict().get('val')
                    ev['value'] = int(val) if val and val.isdigit(
                    ) else m.groupdict().get('val')
                events.append(ev)

        # Find IO calls (read/write) and extract a register candidate
        for m in self._call_re.finditer(func_body):
            call_name = m.group('name')
            args = m.group('args')
            start = m.start()
            line = func_start_line + func_body[:start].count('\n') + 1

            reg_candidate = self._extract_register_from_args(args)
            if filter_reg is not None and filter_reg not in args and filter_reg != reg_candidate:
                continue

            if call_name in self._write_name_set:
                ev_type = 'write'
            elif call_name in self._read_name_set:
                ev_type = 'read'
            else:
                continue

            events.append({
                'type': ev_type,
                'name': call_name,
                'register': reg_candidate,
                'args': self._shorten(args),
                'line': line,
                'index': start,
            })

        # Direct assignment to register macros/identifiers
        if filter_reg:
            assign_re = re.compile(
                self._assign_re_tpl.format(reg=re.escape(filter_reg)))
            for m in assign_re.finditer(func_body):
                start = m.start()
                line = func_start_line + func_body[:start].count('\n') + 1
                events.append({
                    'type': 'write',
                    'name': 'assign',
                    'register': filter_reg,
                    'args': self._shorten(m.group(0)),
                    'line': line,
                    'index': start,
                })

        events.sort(key=lambda e: e.get('index', 0))
        for e in events:
            e.pop('index', None)
        return events

    def _extract_register_from_args(self, args: str) -> Optional[str]:
        # Heuristic: choose prominent uppercase-like macro as register
        # Prefer tokens containing REG, ADDR, OFFS, or ending with _REG
        cand_re = re.compile(r'\b([A-Z][A-Z0-9_]{2,})\b')
        cands = cand_re.findall(args)
        if not cands:
            return None
        # rank candidates

        def rank(tok: str) -> Tuple[int, int]:
            score = 0
            up = tok.upper()
            if up.endswith('_REG'):
                score += 3
            if 'REG' in up:
                score += 2
            if 'ADDR' in up or 'BASE' in up or 'OFF' in up:
                score += 1
            return (score, len(up))
        cands.sort(key=lambda t: rank(t), reverse=True)
        return cands[0] if cands else None

    def _shorten(self, s: str, limit: int = 120) -> str:
        ss = ' '.join(s.strip().split())
        return (ss[:limit] + '...') if len(ss) > limit else ss
