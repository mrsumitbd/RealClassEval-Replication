
import re
from typing import Dict


class PromptCompiler:
    '''Compiles .prompt.md files with parameter substitution.'''

    def __init__(self):
        pass

    def compile(self, prompt_file: str, params: Dict[str, str]) -> str:
        with open(prompt_file, 'r') as file:
            content = file.read()
        return self._substitute_parameters(content, params)

    def _substitute_parameters(self, content: str, params: Dict[str, str]) -> str:
        pattern = re.compile(r'\{\{(\w+)\}\}')

        def replace_match(match):
            param_name = match.group(1)
            return params.get(param_name, match.group(0))
        return pattern.sub(replace_match, content)
