import re
import pathlib
from typing import Dict, Any, List, Optional, Tuple


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
        self.file_contents: Dict[pathlib.Path, str] = dict(file_contents)
        self._func_index: List[Dict[str, Any]] = []
        self._reg_pattern_cache: Dict[str, re.Pattern] = {}
        self._write_tokens = [
            r'\bwritel?\b', r'\bwriteb\b', r'\bwritew\b', r'\biowrite\d*\b',
            r'\bREG_WRITE\b', r'\bSET_BITS?\b', r'\bCLR_BITS?\b', r'\bCLEAR_BITS?\b',
            r'\bset_bit\b', r'\bclear_bit\b', r'\bupdate_bits?\b'
        ]
        self._read_tokens = [
            r'\breadl?\b', r'\breadb\b', r'\breadw\b', r'\bioread\d*\b',
            r'\bREG_READ\b', r'\bget_bits?\b'
        ]
        self._delay_tokens = [
            r'\bmsleep(?:_interruptible)?\b',
            r'\busleep(?:_range)?\b',
            r'\budelay\b',
            r'\bmdelay\b',
            r'\bndelay\b',
            r'\bschedule_timeout(?:_interruptible)?\b',
            r'\bwait_for_(?:completion|event|condition|interruptible)\b',
        ]
        self._parse_functions()

    def _parse_functions(self) -> None:
        func_sig = re.compile(
            r'^[ \t]*(?:[A-Za-z_][\w\s\*\(\)]*?\s+)?([A-Za-z_]\w*)\s*\(([^;{}]*)\)\s*\{',
            re.MULTILINE
        )
        for fpath, content in self.file_contents.items():
            for m in func_sig.finditer(content):
                name = m.group(1)
                brace_start = content.find('{', m.start())
                if brace_start == -1:
                    continue
                end_idx = self._find_matching_brace(content, brace_start)
                if end_idx is None:
                    continue
                # inner body without the outer braces
                inner_body = content[brace_start + 1:end_idx]
                start_line = content.count('\n', 0, brace_start) + 1
                self._func_index.append({
                    'file': fpath,
                    'name': name,
                    'body': inner_body,
                    'start_line': start_line,
                    'signature': content[m.start():brace_start + 1],
                })

    def _find_matching_brace(self, text: str, open_idx: int) -> Optional[int]:
        balance = 0
        i = open_idx
        n = len(text)
        in_char = False
        in_str = False
        esc = False
        while i < n:
            ch = text[i]
            if in_str:
                if esc:
                    esc = False
                elif ch == '\\':
                    esc = True
                elif ch == '"':
                    in_str = False
            elif in_char:
                if esc:
                    esc = False
                elif ch == '\\':
                    esc = True
                elif ch == "'":
                    in_char = False
            else:
                if ch == '"':
                    in_str = True
                elif ch == "'":
                    in_char = True
                elif ch == '{':
                    balance += 1
                elif ch == '}':
                    balance -= 1
                    if balance == 0:
                        return i
            i += 1
        return None

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        '''Get cached function pattern for register name.'''
        key = reg_name
        if key not in self._reg_pattern_cache:
            # Match the register name as a whole word, allowing whitespace/newlines around tokens in macros.
            # Since the identifier itself is not split across lines, this is sufficient.
            pat = re.compile(r'\b' + re.escape(reg_name) + r'\b', re.MULTILINE)
            self._reg_pattern_cache[key] = pat
        return self._reg_pattern_cache[key]

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        '''
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        '''
        pat = self._get_function_pattern(reg_name)
        results: List[Dict[str, Any]] = []
        for fn in self._func_index:
            body = fn['body']
            if not pat.search(body):
                continue
            func_name = fn['name']
            timing = self._determine_timing(func_name, body)
            access = self._analyze_access_pattern(body, reg_name)
            occurrences = list(pat.finditer(body))
            lines = body.splitlines()
            contexts = []
            for m in occurrences:
                line_no = body.count('\n', 0, m.start()) + 1
                window = []
                for ln in range(max(1, line_no - 2), min(len(lines), line_no + 2) + 1):
                    window.append((fn['start_line'] + ln - 1, lines[ln - 1]))
                contexts.append({
                    'line': fn['start_line'] + line_no - 1,
                    'snippet': window
                })
            results.append({
                'file': str(fn['file']),
                'function': func_name,
                'timing': timing,
                'access': access,
                'occurrences': len(occurrences),
                'contexts': contexts
            })
        return {
            'register': reg_name,
            'matches': results
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
        fname = func_name.lower()
        if any(k in fname for k in ['probe', 'init', 'setup', 'config', 'attach']):
            return 'init'
        if any(k in fname for k in ['resume', 'suspend', 'pm', 'power']):
            return 'power'
        if any(k in fname for k in ['irq', 'isr', 'interrupt', 'hardirq', 'softirq']):
            return 'interrupt'
        if any(k in fname for k in ['reset']):
            return 'reset'
        # Fallback: infer from body
        body = func_body
        if re.search(r'\brequest_irq\b|\benable_irq\b|\bdisable_irq\b', body):
            return 'interrupt'
        if re.search(r'\bpm_(?:runtime|suspend|resume)\b', body):
            return 'power'
        if re.search(r'\bmsleep|usleep|udelay|mdelay|ndelay|schedule_timeout\b', body):
            return 'timed_operation'
        return 'runtime'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        '''Analyze register access patterns within a function.'''
        pat = self._get_function_pattern(reg_name)
        write_re = re.compile('|'.join(self._write_tokens), re.IGNORECASE)
        read_re = re.compile('|'.join(self._read_tokens), re.IGNORECASE)
        write_ops = 0
        read_ops = 0
        modify_ops = 0

        for m in pat.finditer(func_body):
            start = max(0, m.start() - 150)
            end = min(len(func_body), m.end() + 150)
            ctx = func_body[start:end]

            # Look for typical write/modify patterns
            if re.search(r'\b(?:\|\=|\&\=|=\s*[^;]*\b' + re.escape(reg_name) + r'\b|write)', ctx) or write_re.search(ctx):
                write_ops += 1
                if re.search(r'\|\=|\&\=|\~', ctx) or re.search(r'\b(update_bits?|set_bits?|clear_bits?)\b', ctx, re.I):
                    modify_ops += 1
            # Look for read patterns
            if re.search(r'\b(?:read|=\s*[^;]*\bread)', ctx) or read_re.search(ctx):
                read_ops += 1
            # Also if line looks like "val = REG" treat as read
            line_start = func_body.rfind('\n', 0, m.start()) + 1
            line_end = func_body.find('\n', m.end())
            if line_end == -1:
                line_end = len(func_body)
            line = func_body[line_start:line_end]
            if re.search(r'=\s*.*\b' + re.escape(reg_name) + r'\b', line):
                read_ops += 1

        if modify_ops > 0:
            return 'modify'
        if write_ops > 0 and read_ops > 0:
            return 'mixed'
        if write_ops > 0:
            return 'write'
        if read_ops > 0:
            return 'read'
        return 'unknown'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''
        Analyze register access sequences with improved function parsing.
        Enhanced to handle nested braces properly using balance counter.
        '''
        results: List[Dict[str, Any]] = []

        # Helper patterns
        write_re = re.compile('|'.join(self._write_tokens), re.IGNORECASE)
        read_re = re.compile('|'.join(self._read_tokens), re.IGNORECASE)
        delay_re = re.compile('|'.join(self._delay_tokens), re.IGNORECASE)

        if reg_name is not None:
            reg_pat = self._get_function_pattern(reg_name)
        else:
            # Try to find likely register tokens in uppercase inside typical access macros
            reg_pat = re.compile(
                r'\b(?:' +
                r'|'.join([r'REG_WRITE', r'writel?', r'writeb', r'writew', r'readl?', r'readb', r'readw',
                           r'SET_BITS?', r'CLR_BITS?', r'CLEAR_BITS?', r'update_bits?']) +
                r')\s*\(\s*([A-Z_][A-Z0-9_]+)\b',
                re.MULTILINE
            )

        for fn in self._func_index:
            body = fn['body']
            lines = body.splitlines()
            base_line = fn['start_line'] - 0  # file line offset

            seq: List[Dict[str, Any]] = []
            if reg_name is not None:
                for idx, line in enumerate(lines, start=1):
                    if not re.search(reg_pat, line):
                        continue
                    op = 'unknown'
                    if write_re.search(line):
                        op = 'write'
                    elif read_re.search(line):
                        op = 'read'
                    if re.search(r'\|\=|\&\=|\~', line, re.I):
                        op = 'modify' if op != 'read' else 'mixed'
                    seq.append({
                        'line': base_line + idx - 1,
                        'text': line.strip(),
                        'op': op,
                        'register': reg_name
                    })
            else:
                for idx, line in enumerate(lines, start=1):
                    m = reg_pat.search(line)
                    if not m:
                        continue
                    reg = m.group(1)
                    op = 'write' if write_re.search(line) else (
                        'read' if read_re.search(line) else 'unknown')
                    seq.append({
                        'line': base_line + idx - 1,
                        'text': line.strip(),
                        'op': op,
                        'register': reg
                    })

            if not seq:
                continue

            timing = self._determine_timing(fn['name'], body)
            delays = []
            for idx, line in enumerate(lines, start=1):
                dm = delay_re.search(line)
                if dm:
                    delays.append(
                        {'line': base_line + idx - 1, 'text': line.strip()})

            results.append({
                'file': str(fn['file']),
                'function': fn['name'],
                'timing': timing,
                'sequence': seq,
                'delays': delays
            })

        return results

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''Analyze timing constraints and delays related to register accesses.'''
        results: List[Dict[str, Any]] = []
        delay_call_re = re.compile(
            r'\b(msleep(?:_interruptible)?|usleep(?:_range)?|udelay|mdelay|ndelay|schedule_timeout(?:_interruptible)?)\s*\(([^;]*)\)\s*;',
            re.IGNORECASE
        )

        # Determine which functions to scan
        if reg_name is not None:
            reg_pat = self._get_function_pattern(reg_name)
        else:
            reg_pat = None

        for fn in self._func_index:
            body = fn['body']
            lines = body.splitlines()
            base_line = fn['start_line']

            # Find access points
            access_points: List[int] = []
            if reg_pat is not None:
                for i, ln in enumerate(lines, start=1):
                    if reg_pat.search(ln):
                        access_points.append(i)
            else:
                # Any line that does read/write to something is an access point
                if not hasattr(self, '_rw_any'):
                    self._rw_any = re.compile(
                        r'\b(?:writel?|writeb|writew|readl?|readb|readw|REG_(?:READ|WRITE)|update_bits?|SET_BITS?|CLR_BITS?|CLEAR_BITS?)\b',
                        re.IGNORECASE
                    )
                for i, ln in enumerate(lines, start=1):
                    if self._rw_any.search(ln):
                        access_points.append(i)

            if not access_points:
                continue

            # For each access point, search a small window afterwards for delays
            for ap in access_points:
                win_start = ap
                win_end = min(len(lines), ap + 6)
                for j in range(win_start, win_end + 1):
                    if j < 1 or j > len(lines):
                        continue
                    dm = delay_call_re.search(lines[j - 1])
                    if not dm:
                        continue
                    delay_call = dm.group(1)
                    delay_arg = dm.group(2).strip()
                    # Collect snippet
                    snippet: List[Tuple[int, str]] = []
                    s_start = max(1, ap - 1)
                    s_end = min(len(lines), j + 1)
                    for k in range(s_start, s_end + 1):
                        snippet.append((base_line + k - 1, lines[k - 1]))
                    results.append({
                        'file': str(fn['file']),
                        'function': fn['name'],
                        'timing': self._determine_timing(fn['name'], body),
                        'access_line': base_line + ap - 1,
                        'delay_line': base_line + j - 1,
                        'delay_call': delay_call,
                        'delay_arg': delay_arg,
                        'register': reg_name if reg_name is not None else None,
                        'snippet': snippet
                    })

        return results
