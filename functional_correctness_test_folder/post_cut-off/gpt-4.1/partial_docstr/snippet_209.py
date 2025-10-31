
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
        self.file_contents = file_contents  # {Path: str}
        self._function_patterns = {}  # reg_name -> re.Pattern
        self._func_decl_pattern = re.compile(
            r'([a-zA-Z_][a-zA-Z0-9_*\s]+)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)\s*\{', re.MULTILINE)
        self._macro_pattern = re.compile(
            r'\\\n', re.MULTILINE)
        self._delay_patterns = [
            re.compile(
                r'\b(msleep|udelay|mdelay|usleep_range|ndelay|cpu_relax|wait_event|schedule_timeout)\b\s*\('),
            re.compile(r'\bfor\s*\(.*?;\s*.*?;\s*.*?\)\s*\{', re.DOTALL)
        ]

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        '''Get cached function pattern for register name.'''
        if reg_name not in self._function_patterns:
            # Match function containing reg_name (as word), with balanced braces
            # We'll use this to find functions that use reg_name
            pattern = re.compile(
                r'([a-zA-Z_][a-zA-Z0-9_*\s]+)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)\s*\{',
                re.MULTILINE)
            self._function_patterns[reg_name] = pattern
        return self._function_patterns[reg_name]

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        '''
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        '''
        result = {}
        for path, content in self.file_contents.items():
            # Preprocess: join macros split across lines
            content_flat = self._macro_pattern.sub('', content)
            # Find all functions
            for func in self._parse_functions(content_flat):
                func_name = func['name']
                func_body = func['body']
                if re.search(r'\b{}\b'.format(re.escape(reg_name)), func_body):
                    timing = self._determine_timing(func_name, func_body)
                    access_pattern = self._analyze_access_pattern(
                        func_body, reg_name)
                    result[func_name] = {
                        'file': str(path),
                        'timing': timing,
                        'access_pattern': access_pattern,
                        'body': func_body
                    }
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
        # Heuristic: if function name or body contains known timing/delay calls
        for pat in self._delay_patterns:
            if pat.search(func_body):
                return 'delayed'
        if re.search(r'\binit\b|\bprobe\b', func_name, re.IGNORECASE):
            return 'initialization'
        if re.search(r'\bexit\b|\bremove\b', func_name, re.IGNORECASE):
            return 'cleanup'
        if re.search(r'\binterrupt\b|\bisr\b', func_name, re.IGNORECASE):
            return 'interrupt'
        return 'normal'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        '''Analyze register access patterns within a function.'''
        # Look for read/write patterns
        read_pat = re.compile(
            r'\b(readl|ioread|inb|inw|inl)\s*\(\s*' + re.escape(reg_name) + r'\b')
        write_pat = re.compile(
            r'\b(writel|iowrite|outb|outw|outl)\s*\(\s*.*\b' + re.escape(reg_name) + r'\b')
        if write_pat.search(func_body) and read_pat.search(func_body):
            return 'read/write'
        elif write_pat.search(func_body):
            return 'write'
        elif read_pat.search(func_body):
            return 'read'
        else:
            # Fallback: check for assignment
            assign_pat = re.compile(r'\b' + re.escape(reg_name) + r'\b\s*=')
            if assign_pat.search(func_body):
                return 'write'
            use_pat = re.compile(r'=\s*' + re.escape(reg_name) + r'\b')
            if use_pat.search(func_body):
                return 'read'
            return 'unknown'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''
        Analyze register access sequences with improved function parsing.
        Enhanced to handle nested braces properly using balance counter.
        '''
        results = []
        for path, content in self.file_contents.items():
            content_flat = self._macro_pattern.sub('', content)
            for func in self._parse_functions(content_flat):
                func_name = func['name']
                func_body = func['body']
                if reg_name is None or re.search(r'\b{}\b'.format(re.escape(reg_name)), func_body):
                    accesses = []
                    # Find all register accesses in order
                    access_pat = re.compile(
                        r'\b(readl|ioread|inb|inw|inl|writel|iowrite|outb|outw|outl)\s*\(([^)]*)\)')
                    for m in access_pat.finditer(func_body):
                        call = m.group(1)
                        args = m.group(2)
                        if reg_name is None or re.search(r'\b{}\b'.format(re.escape(reg_name)), args):
                            accesses.append(
                                {'call': call, 'args': args.strip()})
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
            content_flat = self._macro_pattern.sub('', content)
            for func in self._parse_functions(content_flat):
                func_name = func['name']
                func_body = func['body']
                if reg_name is None or re.search(r'\b{}\b'.format(re.escape(reg_name)), func_body):
                    delays = []
                    for pat in self._delay_patterns:
                        for m in pat.finditer(func_body):
                            delays.append({'delay': m.group(0).strip()})
                    results.append({
                        'file': str(path),
                        'function': func_name,
                        'delays': delays,
                        'body': func_body
                    })
        return results

    def _parse_functions(self, content: str) -> List[Dict[str, str]]:
        '''
        Parse all functions in the given C source content.
        Returns a list of dicts: {'name': ..., 'body': ...}
        Handles nested braces using a balance counter.
        '''
        results = []
        func_decl_pat = self._func_decl_pattern
        for m in func_decl_pat.finditer(content):
            start = m.end() - 1  # position of '{'
            func_name = m.group(2)
            # Find matching closing brace
            brace_count = 1
            i = start + 1
            while i < len(content) and brace_count > 0:
                if content[i] == '{':
                    brace_count += 1
                elif content[i] == '}':
                    brace_count -= 1
                i += 1
            func_body = content[start:i] if brace_count == 0 else content[start:]
            results.append({'name': func_name, 'body': func_body})
        return results
