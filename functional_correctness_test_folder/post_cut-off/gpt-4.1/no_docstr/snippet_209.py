
import re
import pathlib
from typing import Dict, Any, List, Optional


class DriverAnalyzer:

    def __init__(self, file_contents: Dict[pathlib.Path, str]):
        self.file_contents = file_contents
        self.functions = {}  # {func_name: (file_path, func_body)}
        self._parse_functions()

    def _parse_functions(self):
        func_pattern = re.compile(
            r'(?:static\s+)?(?:inline\s+)?(?:\w+\s+)+(\w+)\s*\(([^)]*)\)\s*\{', re.MULTILINE)
        for path, content in self.file_contents.items():
            for match in func_pattern.finditer(content):
                func_name = match.group(1)
                start = match.start()
                body = self._extract_function_body(content, start)
                self.functions[func_name] = (path, body)

    def _extract_function_body(self, content: str, start: int) -> str:
        # Find the function body by matching braces
        brace_count = 0
        in_body = False
        body = []
        for i in range(start, len(content)):
            c = content[i]
            if c == '{':
                brace_count += 1
                in_body = True
            if in_body:
                body.append(c)
            if c == '}':
                brace_count -= 1
                if brace_count == 0 and in_body:
                    break
        return ''.join(body)

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        # Looks for functions that access reg_name (read or write)
        # e.g., REG_NAME =, = REG_NAME, or function calls with REG_NAME
        pattern = re.compile(
            rf'\b(\w+)\s*\([^)]*\)\s*\{{[^}}]*\b{re.escape(reg_name)}\b[^}}]*\}}',
            re.DOTALL
        )
        return pattern

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        result = {}
        for func_name, (path, body) in self.functions.items():
            if re.search(rf'\b{re.escape(reg_name)}\b', body):
                result[func_name] = {
                    'file': str(path),
                    'body': body,
                    'timing': self._determine_timing(func_name, body),
                    'access_pattern': self._analyze_access_pattern(body, reg_name)
                }
        return result

    def _determine_timing(self, func_name: str, func_body: str) -> str:
        # Heuristic: look for delay, sleep, wait, or comment with "timing"
        if re.search(r'\b(delay|sleep|wait|usleep|msleep)\b', func_body):
            return 'delayed'
        if re.search(r'//.*timing|/\*.*timing.*\*/', func_body, re.IGNORECASE | re.DOTALL):
            return 'timing constraint'
        return 'immediate'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        # Heuristic: check for read, write, modify, or sequence
        write_pat = re.compile(rf'\b{re.escape(reg_name)}\b\s*=')
        read_pat = re.compile(rf'=\s*\b{re.escape(reg_name)}\b')
        modify_pat = re.compile(
            rf'\b{re.escape(reg_name)}\b\s*[\+\-\*/]=|[\+\+|\-\-]\s*\b{re.escape(reg_name)}\b')
        if write_pat.search(func_body):
            if modify_pat.search(func_body):
                return 'modify'
            return 'write'
        if read_pat.search(func_body):
            return 'read'
        # Check for function calls with reg_name as argument
        call_pat = re.compile(
            rf'\b\w+\s*\([^)]*\b{re.escape(reg_name)}\b[^)]*\)')
        if call_pat.search(func_body):
            return 'access via call'
        return 'unknown'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        results = []
        for func_name, (path, body) in self.functions.items():
            if reg_name is None or re.search(rf'\b{re.escape(reg_name)}\b', body):
                accesses = []
                lines = body.split('\n')
                for i, line in enumerate(lines):
                    if reg_name is None:
                        # Try to find any register-like access (all-caps with _)
                        reg_match = re.findall(r'\b([A-Z_]{2,})\b', line)
                        for reg in reg_match:
                            if '=' in line:
                                accesses.append(
                                    {'reg': reg, 'type': 'write', 'line': i+1})
                            elif re.search(rf'=\s*{reg}', line):
                                accesses.append(
                                    {'reg': reg, 'type': 'read', 'line': i+1})
                    else:
                        if re.search(rf'\b{re.escape(reg_name)}\b', line):
                            if '=' in line and line.strip().startswith(reg_name):
                                accesses.append(
                                    {'reg': reg_name, 'type': 'write', 'line': i+1})
                            elif re.search(rf'=\s*{re.escape(reg_name)}', line):
                                accesses.append(
                                    {'reg': reg_name, 'type': 'read', 'line': i+1})
                if accesses:
                    results.append({
                        'function': func_name,
                        'file': str(path),
                        'accesses': accesses
                    })
        return results

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        results = []
        for func_name, (path, body) in self.functions.items():
            if reg_name is None or re.search(rf'\b{re.escape(reg_name)}\b', body):
                timing = self._determine_timing(func_name, body)
                if timing != 'immediate':
                    results.append({
                        'function': func_name,
                        'file': str(path),
                        'timing': timing
                    })
        return results
