from typing import Dict
import re
from pathlib import Path


class PromptCompiler:

    def __init__(self):
        self._pattern = re.compile(r"\{\{\s*([a-zA-Z_]\w*)\s*\}\}")

    def compile(self, prompt_file: str, params: Dict[str, str]) -> str:
        content = Path(prompt_file).read_text(encoding="utf-8")
        return self._substitute_parameters(content, params)

    def _substitute_parameters(self, content: str, params: Dict[str, str]) -> str:
        def repl(match: re.Match) -> str:
            key = match.group(1)
            if key not in params:
                raise KeyError(f"Missing parameter: {key}")
            val = params[key]
            return str(val)

        result = self._pattern.sub(repl, content)
        # Check for any unreplaced placeholders
        remaining = self._pattern.findall(result)
        if remaining:
            missing = ", ".join(sorted(set(remaining)))
            raise ValueError(f"Unresolved placeholders: {missing}")
        return result
