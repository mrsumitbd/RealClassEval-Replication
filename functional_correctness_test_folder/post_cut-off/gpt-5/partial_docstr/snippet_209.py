import re
import pathlib
from typing import Dict, Any, Optional, List, Iterable, Tuple


class DriverAnalyzer:
    '''
    Encapsulates driver analysis functionality with shared state.
    This class maintains pre-compiled regex patterns and file content
    to avoid duplication and improve performance.
    '''

    def __init__(self, file_contents: Dict[pathlib.Path, str]):
        self.file_contents: Dict[pathlib.Path, str] = file_contents or {}
        self._func_pattern_cache: Dict[str, re.Pattern] = {}
        self._functions_cache: Dict[pathlib.Path, List[Dict[str, Any]]] = {}
        self._generic_rw_re = re.compile(
            r'(?P<call>\b(?:readl|readw|readb|ioread32|ioread16|ioread8|REG_READ\w*|READ_\w*|'
            r'writel|writew|writeb|iowrite32|iowrite16|iowrite8|REG_WRITE\w*|WRITE_\w*))'
            r'\s*\((?P<args>[^;]*?)\)',
            re.IGNORECASE,
        )
        self._delay_re = re.compile(
            r'\b(?:udelay|mdelay|ndelay|msleep|usleep_range|fsleep|usleep)\b\s*\((?P<val>[^)]*)\)',
            re.IGNORECASE,
        )
        self._comment_delay_hint_re = re.compile(
            r'//.*?\b(delay|wait|timing|settle)\b|/\*.*?\b(delay|wait|timing|settle)\b.*?\*/',
            re.IGNORECASE | re.DOTALL,
        )
        self._func_header_re = re.compile(
            r'^[ \t]*(?:[A-Za-z_][\w\s\*\(\),]*?\s+)?(?P<name>[A-Za-z_]\w*)\s*\([^;{]*\)\s*\{',
            re.MULTILINE,
        )
        self._ctrl_keywords = {'if', 'for', 'while', 'switch', 'do'}

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        '''Get cached function pattern for register name.'''
        if reg_name in self._func_pattern_cache:
            return self._func_pattern_cache[reg_name]
        reg_esc = re.escape(reg_name)
        direct = rf'\b{reg_esc}\b'
        macro = rf'(?s)\b(?:SET|CLR|WRITE|READ|UPDATE|MODIFY)\w*\s*\(\s*[^)]*\b{reg_esc}\b'
        pat = re.compile(f'(?:{direct}|{macro})', re.IGNORECASE)
        self._func_pattern_cache[reg_name] = pat
        return pat

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        '''
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        '''
        result: Dict[str, Any] = {
            'register': reg_name,
            'occurrences': [],
            'total_functions': 0,
        }
        pat = self._get_function_pattern(reg_name)
        for fpath, funcs in self._iter_all_functions():
            for f in funcs:
                body = f['body']
                if pat.search(body):
                    timing = self._determine_timing(f['name'], body)
                    access = self._analyze_access_pattern(body, reg_name)
                    count = len(re.findall(
                        self._get_function_pattern(reg_name), body))
                    result['occurrences'].append({
                        'file': str(fpath),
                        'function': f['name'],
                        'line_start': f['line_start'],
                        'line_end': f['line_end'],
                        'usage_count': count,
                        'access_pattern': access,
                        'timing': timing,
                    })
                    result['total_functions'] += 1
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
        name_l = func_name.lower()
        if any(k in name_l for k in ('probe', 'init', 'attach', 'open', 'power_on')):
            return 'init'
        if any(k in name_l for k in ('remove', 'detach', 'exit', 'close', 'power_off', 'shutdown')):
            return 'deinit'
        if any(k in name_l for k in ('suspend',)):
            return 'suspend'
        if any(k in name_l for k in ('resume', 'restore')):
            return 'resume'
        if any(k in name_l for k in ('irq', 'isr', 'interrupt', 'handler')):
            return 'interrupt'
        if any(k in name_l for k in ('reset', 'reinit')):
            return 'reset'
        if any(k in name_l for k in ('set_rate', 'clk', 'clock')):
            return 'clock_config'
        if any(k in name_l for k in ('config', 'configure', 'setup')):
            return 'config'

        if self._delay_re.search(func_body):
            return 'delay_sensitive'
        if re.search(r'\b(enable|disable)_(clk|clock)\b', func_body):
            return 'clock_control'
        if re.search(r'\bgpiod?_(set|direction|to)_', func_body):
            return 'gpio_control'
        if re.search(r'\bpower_(on|off|enable|disable)\b', func_body):
            return 'power_transition'
        if self._comment_delay_hint_re.search(func_body):
            return 'timing_hinted'

        return 'general'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        '''Analyze register access patterns within a function.'''
        body = func_body
        reg_esc = re.escape(reg_name)
        write_calls = re.findall(
            rf'\b(?:writel|writew|writeb|iowrite\d+|REG_WRITE\w*|WRITE_\w*)\b[^\S\r\n]*\([^\)]*\b{reg_esc}\b',
            body, re.IGNORECASE | re.DOTALL
        )
        read_calls = re.findall(
            rf'\b(?:readl|readw|readb|ioread\d+|REG_READ\w*|READ_\w*)\b[^\S\r\n]*\([^\)]*\b{reg_esc}\b',
            body, re.IGNORECASE | re.DOTALL
        )
        direct_write = re.findall(
            rf'\b{reg_esc}\b\s*(?:\|\=|\&\=|\^\=|=|<<=|>>=)', body)
        direct_read = re.findall(
            rf'(?:\W|^)\b{reg_esc}\b\s*(?:[|&^]|<<|>>)', body)
        has_write = bool(write_calls or direct_write)
        has_read = bool(read_calls or direct_read)

        if has_read and has_write:
            # Check for typical read-modify-write sequence
            rmw = re.search(
                rf'(readl|REG_READ\w*|READ_\w*).*?{reg_esc}.*?(writel|REG_WRITE\w*|WRITE_\w*)',
                body, re.IGNORECASE | re.DOTALL
            )
            return 'read-modify-write' if rmw else 'mixed'
        if has_write:
            return 'write-only'
        if has_read:
            return 'read-only'
        return 'unknown'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''
        Analyze register access sequences with improved function parsing.
        Enhanced to handle nested braces properly using balance counter.
        '''
        results: List[Dict[str, Any]] = []
        reg_pat = self._get_function_pattern(reg_name) if reg_name else None

        for fpath, funcs in self._iter_all_functions():
            for f in funcs:
                body = f['body']
                if reg_pat and not reg_pat.search(body):
                    continue
                seq: List[Dict[str, Any]] = []
                line_offsets = self._compute_line_offsets(f['full_text'])
                body_start_offset = f['body_start_offset_in_full']
                for m in self._generic_rw_re.finditer(body):
                    call = m.group('call')
                    args = m.group('args') or ''
                    call_l = call.lower()
                    acc_type = 'read' if call_l.startswith(
                        'read') or 'ioread' in call_l else 'write'
                    reg_in_args = self._extract_reg_from_args(args)
                    if reg_name and (not reg_in_args or reg_in_args != reg_name):
                        # If we expected a specific reg but didn't match, skip
                        continue
                    # approximate line number
                    abs_pos = body_start_offset + m.start()
                    line_no = self._offset_to_line(line_offsets, abs_pos)
                    seq.append({
                        'type': acc_type,
                        'call': call,
                        'args': args.strip(),
                        'register': reg_in_args,
                        'line': line_no,
                    })
                if seq:
                    results.append({
                        'file': str(fpath),
                        'function': f['name'],
                        'line_start': f['line_start'],
                        'line_end': f['line_end'],
                        'sequence': seq,
                    })
        return results

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''Analyze timing constraints and delays related to register accesses.'''
        results: List[Dict[str, Any]] = []
        reg_pat = self._get_function_pattern(reg_name) if reg_name else None

        for fpath, funcs in self._iter_all_functions():
            for f in funcs:
                body = f['body']
                if reg_pat and not reg_pat.search(body):
                    continue
                delays = []
                for m in self._delay_re.finditer(body):
                    val = (m.group('val') or '').strip()
                    abs_pos = f['body_start_offset_in_full'] + m.start()
                    line_no = self._offset_to_line(
                        self._compute_line_offsets(f['full_text']), abs_pos)
                    delays.append({'call': m.group(0).split(
                        '(')[0].strip(), 'value': val, 'line': line_no})
                hinted = bool(self._comment_delay_hint_re.search(body))
                if delays or hinted or (reg_pat is not None):
                    timing = self._determine_timing(f['name'], body)
                    results.append({
                        'file': str(fpath),
                        'function': f['name'],
                        'line_start': f['line_start'],
                        'line_end': f['line_end'],
                        'timing': timing,
                        'delays': delays,
                        'comment_hints': hinted,
                    })
        return results

    # Internal helpers

    def _iter_all_functions(self) -> Iterable[Tuple[pathlib.Path, List[Dict[str, Any]]]]:
        for fpath, text in self.file_contents.items():
            if fpath not in self._functions_cache:
                self._functions_cache[fpath] = list(
                    self._extract_functions(text))
            yield fpath, self._functions_cache[fpath]

    def _extract_functions(self, text: str) -> Iterable[Dict[str, Any]]:
        for m in self._func_header_re.finditer(text):
            name = m.group('name')
            if name in self._ctrl_keywords:
                continue
            brace_start = text.find('{', m.end() - 1)
            if brace_start == -1:
                continue
            body, end_idx = self._extract_balanced_block(text, brace_start)
            if body is None:
                continue
            header_start = m.start()
            header_end = brace_start + 1
            line_start = text.count('\n', 0, header_start) + 1
            line_end = text.count('\n', 0, end_idx) + 1
            yield {
                'name': name,
                'header': text[header_start:header_end],
                'body': body,
                'full_text': text[header_start:end_idx],
                'line_start': line_start,
                'line_end': line_end,
                'body_start_offset_in_full': header_start,
            }

    def _extract_balanced_block(self, text: str, start_brace_idx: int) -> Tuple[Optional[str], Optional[int]]:
        depth = 0
        i = start_brace_idx
        n = len(text)
        in_str = None
        in_char = False
        in_sl_comment = False
        in_ml_comment = False
        while i < n:
            ch = text[i]
            nxt = text[i + 1] if i + 1 < n else ''
            if in_sl_comment:
                if ch == '\n':
                    in_sl_comment = False
                i += 1
                continue
            if in_ml_comment:
                if ch == '*' and nxt == '/':
                    in_ml_comment = False
                    i += 2
                    continue
                i += 1
                continue
            if in_str:
                if ch == '\\':
                    i += 2
                    continue
                if ch == in_str:
                    in_str = None
                i += 1
                continue
            if in_char:
                if ch == '\\':
                    i += 2
                    continue
                if ch == "'":
                    in_char = False
                i += 1
                continue

            if ch == '/' and nxt == '/':
                in_sl_comment = True
                i += 2
                continue
            if ch == '/' and nxt == '*':
                in_ml_comment = True
                i += 2
                continue
            if ch == '"' or ch == 'L' and nxt == '"':
                in_str = '"'
                i += 1
                continue
            if ch == "'":
                in_char = True
                i += 1
                continue

            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    body = text[start_brace_idx + 1:i]
                    return body, i + 1
            i += 1
        return None, None

    def _compute_line_offsets(self, text: str) -> List[int]:
        offsets = [0]
        for m in re.finditer(r'\n', text):
            offsets.append(m.end())
        return offsets

    def _offset_to_line(self, line_offsets: List[int], pos: int) -> int:
        # binary search
        lo, hi = 0, len(line_offsets)
        while lo < hi:
            mid = (lo + hi) // 2
            if line_offsets[mid] <= pos:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def _extract_reg_from_args(self, args: str) -> Optional[str]:
        # Heuristic: prefer tokens like REG_* or register-like identifiers
        tokens = re.findall(r'\b[A-Za-z_]\w*\b', args)
        if not tokens:
            return None
        # Prioritize REG_* style
        for t in tokens:
            if t.isupper() and ('REG' in t or 'CTRL' in t or 'CFG' in t or 'ADDR' in t):
                return t
        # Else, return first identifier that looks like a register macro/var
        return tokens[0] if tokens else None
