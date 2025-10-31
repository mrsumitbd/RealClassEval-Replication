
from typing import Dict
import re


class PromptCompiler:

    def __init__(self):
        pass

    def compile(self, prompt_file: str, params: Dict[str, str]) -> str:
        try:
            with open(prompt_file, 'r') as file:
                content = file.read()
                return self._substitute_parameters(content, params)
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {prompt_file} was not found.")

    def _substitute_parameters(self, content: str, params: Dict[str, str]) -> str:
        pattern = r'\{(.*?)\}'
        return re.sub(pattern, lambda match: params.get(match.group(1), match.group(0)), content)
