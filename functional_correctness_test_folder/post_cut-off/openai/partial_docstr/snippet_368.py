
import re
from typing import Dict


class PromptCompiler:
    '''Compiles .prompt.md files with parameter substitution.'''

    def __init__(self):
        # Precompile the placeholder pattern: {{param}}
        self._placeholder_pattern = re.compile(r'\{\{(\w+)\}\}')

    def compile(self, prompt_file: str, params: Dict[str, str]) -> str:
        """
        Read the prompt file, substitute parameters, and return the compiled content.

        :param prompt_file: Path to the .prompt.md file.
        :param params: Dictionary of parameter names to values.
        :return: The compiled prompt content as a string.
        """
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        return self._substitute_parameters(content, params)

    def _substitute_parameters(self, content: str, params: Dict[str, str]) -> str:
        """
        Replace all placeholders in the form {{key}} with the corresponding value from params.

        :param content: The raw content containing placeholders.
        :param params: Dictionary of parameter names to values.
        :return: The content with placeholders substituted.
        :raises KeyError: If a placeholder key is not found in params.
        """
        def repl(match: re.Match) -> str:
            key = match.group(1)
            if key not in params:
                raise KeyError(
                    f"Missing parameter for placeholder '{{{{{key}}}}}'")
            return str(params[key])

        return self._placeholder_pattern.sub(repl, content)
