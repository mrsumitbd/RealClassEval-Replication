from typing import Dict, List, Type, Optional, Callable, Union, Any
import re

class RoutePattern:
    """Handles route pattern matching with parameters and wildcards."""

    def __init__(self, pattern: str):
        self.pattern = pattern
        self.param_names = []
        self.regex_pattern = self._compile_pattern()

    def _compile_pattern(self) -> re.Pattern:
        """Compile route pattern to regex."""
        pattern = self.pattern
        param_pattern = ':([a-zA-Z_][a-zA-Z0-9_]*)'
        matches = re.findall(param_pattern, pattern)
        self.param_names = matches
        regex_pattern = re.sub(param_pattern, '([^/]+)', pattern)
        regex_pattern = regex_pattern.replace('*', '(.*)')
        regex_pattern = f'^{regex_pattern}$'
        return re.compile(regex_pattern)

    def match(self, path: str) -> Optional[Dict[str, str]]:
        """Match path against pattern and extract parameters."""
        match = self.regex_pattern.match(path)
        if not match:
            return None
        params = {}
        for i, param_name in enumerate(self.param_names):
            params[param_name] = match.group(i + 1)
        return params