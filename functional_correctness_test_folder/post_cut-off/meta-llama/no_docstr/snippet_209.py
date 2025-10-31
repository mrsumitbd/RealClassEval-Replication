
import pathlib
import re
from typing import Dict, Any, List, Optional


class DriverAnalyzer:

    def __init__(self, file_contents: Dict[pathlib.Path, str]):
        self.file_contents = file_contents

    def _get_function_pattern(self, reg_name: str) -> re.Pattern:
        return re.compile(rf'def\s+({reg_name}_\w+)\s*\((.*?)\)', re.DOTALL)

    def analyze_function_context(self, reg_name: str) -> Dict[str, Any]:
        pattern = self._get_function_pattern(reg_name)
        results = {}
        for file_path, content in self.file_contents.items():
            for match in pattern.finditer(content):
                func_name = match.group(1)
                func_body = match.group(0)
                results[func_name] = {
                    'file_path': file_path,
                    'function_body': func_body,
                    'timing': self._determine_timing(func_name, func_body)
                }
        return results

    def _determine_timing(self, func_name: str, func_body: str) -> str:
        # Simple timing analysis based on the presence of 'time.sleep' or 'delay'
        if 'time.sleep' in func_body or 'delay' in func_body:
            return 'async'
        else:
            return 'sync'

    def _analyze_access_pattern(self, func_body: str, reg_name: str) -> str:
        # Simple access pattern analysis based on the presence of 'read' or 'write'
        if f'{reg_name}.read' in func_body:
            return 'read'
        elif f'{reg_name}.write' in func_body:
            return 'write'
        else:
            return 'unknown'

    def analyze_access_sequences(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        results = []
        for file_path, content in self.file_contents.items():
            functions = self.analyze_function_context(reg_name or '')
            for func_name, func_info in functions.items():
                if reg_name is None or reg_name in func_name:
                    access_pattern = self._analyze_access_pattern(
                        func_info['function_body'], reg_name or '')
                    results.append({
                        'register_name': reg_name,
                        'function_name': func_name,
                        'file_path': func_info['file_path'],
                        'access_pattern': access_pattern
                    })
        return results

    def analyze_timing_constraints(self, reg_name: Optional[str] = None) -> List[Dict[str, Any]]:
        results = []
        for file_path, content in self.file_contents.items():
            functions = self.analyze_function_context(reg_name or '')
            for func_name, func_info in functions.items():
                if reg_name is None or reg_name in func_name:
                    results.append({
                        'register_name': reg_name,
                        'function_name': func_name,
                        'file_path': func_info['file_path'],
                        'timing': func_info['timing']
                    })
        return results
