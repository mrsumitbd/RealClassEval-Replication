
from typing import Dict


class PromptCompiler:

    def __init__(self):
        pass

    def compile(self, prompt_file: str, params: Dict[str, str]) -> str:
        with open(prompt_file, 'r') as file:
            content = file.read()
        return self._substitute_parameters(content, params)

    def _substitute_parameters(self, content: str, params: Dict[str, str]) -> str:
        for key, value in params.items():
            content = content.replace(f'{{{key}}}', value)
        return content
