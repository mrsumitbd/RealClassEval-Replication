
import pathlib
import re
from typing import Dict, Any, List, Optional, Tuple


class DriverAnalyzer:
    """
    Simple driver analysis utility that scans Python source files for
    functions that access a given register name and reports basic
    access patterns and timing hints.
    """

    def __init__(self, file_contents: Dict[pathlib.Path, str]):
        """
        :param file_contents: Mapping from file path to file content string.
        """
        self.file_contents = file_contents
        # Pre‑compile the function definition regex once
        self._func_def_re = re.compile(
            r'^\s*def\s+(\w+)\s*\(.*\):', re.MULTILINE)

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        """
        Return a regex pattern that matches any function definition that
        contains the given register name in its body.
        """
        # We will use the pre‑compiled function definition regex and
        # then filter by body content later.
        return self._func_def_re

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        """
        Analyze all functions that reference the given register name.
        Returns a dictionary containing a list of function contexts.
        """
        contexts = []
        for file_path, content in self.file_contents.items():
            for func_name, body, start_line in self._extract_functions(content):
                if reg_name in body:
                    access_pattern = self._analyze_access_pattern(
                        body, reg_name)
                    timing = self._determine_timing(func_name, body)
                    contexts.append({
                        'function': func_name,
                        'file': str(file_path),
                        'start_line': start_line,
                        'access_pattern': access_pattern,
                        'timing': timing,
                    })
        return {'functions': contexts}

    def _determine_timing(self, func_name: str, func_body: str) -> str:
        """
        Very naive timing determination based on function name.
        """
        name_lower = func_name.lower()
        if any(keyword in name_lower for keyword in ('clk', 'clock', 'edge', 'tick')):
            return 'edge'
        return 'unknown'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        """
        Determine if the register is read, written, or both.
        """
        read = False
        write = False
        reg_pattern = re.compile(r'\b' + re.escape(reg_name) + r'\b')
        write_pattern = re.compile(r'\b' + re.escape(reg_name) + r'\b\s*=')
        for line in func_body.splitlines():
            if reg_pattern.search(line):
                read = True
            if write_pattern.search(line):
                write = True
        if read and write:
            return 'read_write'
        if write:
            return 'write'
        if read:
            return 'read'
        return 'none'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Return a list of access sequence dictionaries for the given register.
        If reg_name is None, analyze all registers found in the code.
        """
        sequences = []
        for file_path, content in self.file_contents.items():
            for func_name, body, start_line in self._extract_functions(content):
                if reg_name is None:
                    # Find all register names in the body
                    regs = set(re.findall(
                        r'\b([A-Za-z_][A-Za-z0-9_]*)\b', body))
                else:
                    regs = {reg_name}
                for reg in regs:
                    if reg in body:
                        access_pattern = self._analyze_access_pattern(
                            body, reg)
                        timing = self._determine_timing(func_name, body)
                        sequences.append({
                            'function': func_name,
                            'file': str(file_path),
                            'start_line': start_line,
                            'register': reg,
                            'access_pattern': access_pattern,
                            'timing': timing,
                        })
        return sequences

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Return a list of timing constraint dictionaries for the given register.
        If reg_name is None, analyze all registers found in the code.
        """
        constraints = []
        for file_path, content in self.file_contents.items():
            for func_name, body, start_line in self._extract_functions(content):
                if reg_name is None:
                    regs = set(re.findall(
                        r'\b([A-Za-z_][A-Za-z0-9_]*)\b', body))
                else:
                    regs = {reg_name}
                for reg in regs:
                    if reg in body:
                        timing = self._determine_timing(func_name, body)
                        constraints.append({
                            'function': func_name,
                            'file': str(file_path),
                            'start_line': start_line,
                            'register': reg,
                            'timing': timing,
                        })
        return constraints

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------
    def _extract_functions(self, content: str) -> List[Tuple[str, str, int]]:
        """
        Extract function definitions from the given content.
        Returns a list of tuples: (function_name, body, start_line_number).
        """
        functions = []
        lines = content.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            match = self._func_def_re.match(line)
            if match:
                func_name = match.group(1)
                start_line = i + 1  # 1‑based line number
                # Determine indentation level
                indent = len(line) - len(line.lstrip())
                body_lines = []
                i += 1
                while i < len(lines):
                    next_line = lines[i]
                    # Empty lines are part of the body
                    if next_line.strip() == '':
                        body_lines.append(next_line)
                        i += 1
                        continue
                    next_indent = len(next_line) - len(next_line.lstrip())
                    if next_indent > indent:
                        body_lines.append(next_line)
                        i += 1
                    else:
                        break
                body = '\n'.join(body_lines)
                functions.append((func_name, body, start_line))
            else:
                i += 1
        return functions
