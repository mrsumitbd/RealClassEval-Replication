
import pathlib
import re
from typing import Any, Dict, List, Optional, Pattern


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
        self._func_pattern_cache: Dict[str, Pattern] = {}
        self._functions: Dict[str, str] = {}
        self._parse_all_functions()

    def _get_function_pattern(self, reg_name: str) -> Pattern:
        '''Get cached function pattern for register name.'''
        # The pattern is independent of reg_name; cache by a fixed key
        key = "func_def"
        if key not in self._func_pattern_cache:
            # Matches typical C function definitions
            self._func_pattern_cache[key] = re.compile(
                r'\b(?:void|int|char|float|double|unsigned|signed)\s+(\w+)\s*\([^)]*\)\s*{',
                re.MULTILINE
            )
        return self._func_pattern_cache[key]

    def _parse_all_functions(self) -> None:
        '''Populate self._functions with function name -> body mapping.'''
        func_pat = self._get_function_pattern("")
        for content in self.file_contents.values():
            for match in func_pat.finditer(content):
                func_name = match.group(1)
                start = match.end()  # position after '{'
                # Find matching closing brace using a simple stack
                brace_count = 1
                pos = start
                while pos < len(content) and brace_count:
                    if content[pos] == '{':
                        brace_count += 1
                    elif content[pos] == '}':
                        brace_count -= 1
                    pos += 1
                body = content[start:pos-1]  # exclude closing '}'
                self._functions[func_name] = body

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        '''
        Analyze the function context where a register is used.
        Enhanced to recognize macros split across lines and provide
        fallback timing detection.
        '''
        for func_name, body in self._functions.items():
            if reg_name in body:
                timing = self._determine_timing(func_name, body)
                access_pattern = self._analyze_access_pattern(body, reg_name)
                return {
                    "function": func_name,
                    "timing": timing,
                    "access_pattern": access_pattern,
                }
        return {"function": None, "timing": None, "access_pattern": None}

    def _determine_timing(self, func_name: str, func_body: str) -> str:
        '''
        Determine timing context with fallback detection.
        Args:
            func_name: Name of the function
            func_body: Content of the function
        Returns:
            Timing classification string
        '''
        # Look for common delay or wait calls
        async_patterns = [
            r'\bdelay\b',
            r'\bsleep\b',
            r'\bmsleep\b',
            r'\busleep\b',
            r'\bwait\b',
            r'\bpoll\b',
        ]
        for pat in async_patterns:
            if re.search(pat, func_body):
                return "asynchronous"

        # Look for edge-triggered constructs (simplified)
        if re.search(r'\bposedge\b', func_body) or re.search(r'\bnegedge\b', func_body):
            return "synchronous"

        return "unknown"

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        '''Analyze register access patterns within a function.'''
        # Count writes (assignment to reg_name) and reads (usage without assignment)
        write_pat = re.compile(rf'\b{re.escape(reg_name)}\s*=')
        read_pat = re.compile(rf'\b{re.escape(reg_name)}\b')

        writes = len(write_pat.findall(func_body))
        reads = len(read_pat.findall(func_body)) - writes

        if writes and reads:
            return "read-write"
        if writes:
            return "write-only"
        if reads:
            return "read-only"
        return "unknown"

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''
        Analyze register access sequences with improved function parsing.
        Enhanced to handle nested braces properly using balance counter.
        '''
        results = []
        for func_name, body in self._functions.items():
            if reg_name and reg_name not in body:
                continue
            accesses = []
            # Simple regex to find all occurrences of reg_name
            for m in re.finditer(rf'\b{re.escape(reg_name)}\b', body):
                # Determine if it's a write or read
                before = body[:m.start()].rstrip()
                if before.endswith('='):
                    access_type = "write"
                else:
                    access_type = "read"
                accesses.append({"type": access_type, "position": m.start()})
            if accesses:
                results.append({
                    "function": func_name,
                    "accesses": accesses,
                })
        return results

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        '''Analyze timing constraints and delays related to register accesses.'''
        results = []
        delay_pat = re.compile(r'\b(delay|sleep|msleep|usleep|wait|poll)\b')
        for func_name, body in self._functions.items():
            if reg_name and reg_name not in body:
                continue
            delays = []
            for m in delay_pat.finditer(body):
                delays.append({"call": m.group(0), "position": m.start()})
            if delays:
                results.append({
                    "function": func_name,
                    "delays": delays,
                })
        return results
