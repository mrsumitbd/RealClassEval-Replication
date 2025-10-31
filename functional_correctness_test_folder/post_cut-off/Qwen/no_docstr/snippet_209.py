
import re
from typing import Dict, Any, List, Optional
import pathlib


class DriverAnalyzer:

    def __init__(self, file_contents: Dict[pathlib.Path, str]):
        self.file_contents = file_contents

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        return re.compile(rf'def\s+{reg_name}\s*\((.*?)\):\s*(.*?)\n\s*def', re.DOTALL)

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        pattern = self._get_function_pattern(reg_name)
        results = {}
        for file_path, content in self.file_contents.items():
            matches = pattern.findall(content)
            for match in matches:
                args, body = match
                results[file_path.name] = {
                    'args': args,
                    'body': body.strip()
                }
        return results

    def _determine_timing(self, func_name: str, func_body: str) -> str:
        if 'time.sleep' in func_body:
            return 'delayed'
        elif 'async' in func_name or 'await' in func_body:
            return 'asynchronous'
        else:
            return 'synchronous'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        read_pattern = re.compile(rf'{reg_name}\s*=')
        write_pattern = re.compile(rf'\b{reg_name}\b')
        reads = len(read_pattern.findall(func_body))
        writes = len(write_pattern.findall(func_body)) - reads
        if reads > writes:
            return 'read-heavy'
        elif writes > reads:
            return 'write-heavy'
        else:
            return 'balanced'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        sequences = []
        for file_path, content in self.file_contents.items():
            functions = re.findall(
                r'def\s+(\w+)\s*\((.*?)\):\s*(.*?)\n\s*def', content, re.DOTALL)
            for func_name, args, body in functions:
                if reg_name is None or reg_name in body:
                    access_pattern = self._analyze_access_pattern(
                        body, reg_name)
                    sequences.append({
                        'file': file_path.name,
                        'function': func_name,
                        'access_pattern': access_pattern
                    })
        return sequences

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        constraints = []
        for file_path, content in self.file_contents.items():
            functions = re.findall(
                r'def\s+(\w+)\s*\((.*?)\):\s*(.*?)\n\s*def', content, re.DOTALL)
            for func_name, args, body in functions:
                if reg_name is None or reg_name in body:
                    timing = self._determine_timing(func_name, body)
                    constraints.append({
                        'file': file_path.name,
                        'function': func_name,
                        'timing': timing
                    })
        return constraints
