
import re
import pathlib
from typing import Dict, Any, List, Optional, Pattern


class DriverAnalyzer:

    def __init__(self, file_contents: Dict[pathlib.Path, str]):
        self.file_contents = file_contents

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        return re.compile(rf'void\s+\w*{reg_name}\w*\s*\([^)]*\)\s*{{([^}}]*)}}', re.MULTILINE | re.DOTALL)

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        pattern = self._get_function_pattern(reg_name)
        results = {}
        for file_path, content in self.file_contents.items():
            matches = pattern.finditer(content)
            for match in matches:
                func_name = match.group(0).split('(')[0].split()[-1]
                func_body = match.group(1)
                results[func_name] = {
                    'file': str(file_path),
                    'body': func_body
                }
        return results

    def _determine_timing(self, func_name: str, func_body: str) -> str:
        if 'delay' in func_body.lower() or 'sleep' in func_body.lower():
            return 'asynchronous'
        else:
            return 'synchronous'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        if func_body.count(reg_name) > 1:
            return 'multiple'
        else:
            return 'single'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        results = []
        if reg_name is None:
            for file_path, content in self.file_contents.items():
                functions = re.finditer(
                    r'void\s+(\w+)\s*\([^)]*\)\s*{([^}]*)}', content, re.MULTILINE | re.DOTALL)
                for func in functions:
                    func_name = func.group(1)
                    func_body = func.group(2)
                    results.append({
                        'function': func_name,
                        'file': str(file_path),
                        'access_pattern': 'unknown'
                    })
        else:
            func_context = self.analyze_function_context(reg_name)
            for func_name, data in func_context.items():
                access_pattern = self._analyze_access_pattern(
                    data['body'], reg_name)
                results.append({
                    'function': func_name,
                    'file': data['file'],
                    'access_pattern': access_pattern
                })
        return results

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        results = []
        if reg_name is None:
            for file_path, content in self.file_contents.items():
                functions = re.finditer(
                    r'void\s+(\w+)\s*\([^)]*\)\s*{([^}]*)}', content, re.MULTILINE | re.DOTALL)
                for func in functions:
                    func_name = func.group(1)
                    func_body = func.group(2)
                    timing = self._determine_timing(func_name, func_body)
                    results.append({
                        'function': func_name,
                        'file': str(file_path),
                        'timing': timing
                    })
        else:
            func_context = self.analyze_function_context(reg_name)
            for func_name, data in func_context.items():
                timing = self._determine_timing(func_name, data['body'])
                results.append({
                    'function': func_name,
                    'file': data['file'],
                    'timing': timing
                })
        return results
