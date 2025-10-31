
import pathlib
import re
from typing import Dict, Any, List, Optional


class DriverAnalyzer:

    def __init__(self, file_contents: Dict[pathlib.Path, str]):
        self.file_contents = file_contents

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        pattern = rf'void\s+{reg_name}_driver\s*\(.*?\)\s*\{{(.*?)\}}'
        return re.compile(pattern, re.DOTALL)

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        context = {}
        for file_path, content in self.file_contents.items():
            pattern = self._get_function_pattern(reg_name)
            match = pattern.search(content)
            if match:
                func_body = match.group(1)
                context[file_path] = {
                    'function_body': func_body,
                    'timing': self._determine_timing(reg_name, func_body),
                    'access_pattern': self._analyze_access_pattern(func_body, reg_name)
                }
        return context

    def _determine_timing(self, func_name: str, func_body: str) -> str:
        if 'clock' in func_body.lower():
            return 'clock'
        elif 'delay' in func_body.lower():
            return 'delay'
        else:
            return 'unknown'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        if f'read_{reg_name}' in func_body.lower():
            return 'read'
        elif f'write_{reg_name}' in func_body.lower():
            return 'write'
        else:
            return 'unknown'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        sequences = []
        for file_path, content in self.file_contents.items():
            if reg_name:
                pattern = self._get_function_pattern(reg_name)
                matches = pattern.finditer(content)
            else:
                pattern = re.compile(
                    r'void\s+\w+_driver\s*\(.*?\)\s*\{{(.*?)\}}', re.DOTALL)
                matches = pattern.finditer(content)
            for match in matches:
                func_body = match.group(1)
                sequences.append({
                    'file_path': file_path,
                    'function_body': func_body,
                    'access_pattern': self._analyze_access_pattern(func_body, reg_name) if reg_name else 'unknown'
                })
        return sequences

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        constraints = []
        for file_path, content in self.file_contents.items():
            if reg_name:
                pattern = self._get_function_pattern(reg_name)
                matches = pattern.finditer(content)
            else:
                pattern = re.compile(
                    r'void\s+\w+_driver\s*\(.*?\)\s*\{{(.*?)\}}', re.DOTALL)
                matches = pattern.finditer(content)
            for match in matches:
                func_body = match.group(1)
                constraints.append({
                    'file_path': file_path,
                    'function_body': func_body,
                    'timing': self._determine_timing(reg_name, func_body) if reg_name else 'unknown'
                })
        return constraints
