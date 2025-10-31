from typing import Dict
import os
import re


class PromptCompiler:
    '''Compiles .prompt.md files with parameter substitution.'''
    _PLACEHOLDER_RE = re.compile(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}")

    def __init__(self):
        pass

    def compile(self, prompt_file: str, params: Dict[str, str]) -> str:
        if not os.path.exists(prompt_file):
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
        with open(prompt_file, "r", encoding="utf-8") as f:
            content = f.read()
        return self._substitute_parameters(content, params)

    def _substitute_parameters(self, content: str, params: Dict[str, str]) -> str:
        def replacer(match: re.Match) -> str:
            key = match.group(1)
            if key not in params:
                raise ValueError(f"Missing parameter: '{key}'")
            value = params[key]
            return "" if value is None else str(value)

        return self._PLACEHOLDER_RE.sub(replacer, content)
