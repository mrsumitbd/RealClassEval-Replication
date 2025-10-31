
import re
from typing import Dict


class PromptCompiler:
    '''Compiles .prompt.md files with parameter substitution.'''

    def __init__(self):
        pass

    def compile(self, prompt_file: str, params: Dict[str, str]) -> str:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        return self._substitute_parameters(content, params)

    def _substitute_parameters(self, content: str, params: Dict[str, str]) -> str:
        def replacer(match):
            key = match.group(1)
            return params.get(key, match.group(0))
        pattern = re.compile(r'\{\{(\w+)\}\}')
        return pattern.sub(replacer, content)
