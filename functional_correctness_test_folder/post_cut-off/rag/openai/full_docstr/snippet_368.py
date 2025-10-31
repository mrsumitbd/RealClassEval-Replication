
import os
import re
from typing import Dict


class PromptCompiler:
    '''Compiles .prompt.md files with parameter substitution.'''

    def __init__(self):
        '''Initialize compiler.'''
        # No state needed for this simple compiler
        pass

    def compile(self, prompt_file: str, params: Dict[str, str]) -> str:
        '''Compile a .prompt.md file with parameter substitution.
        Args:
            prompt_file: Path to the .prompt.md file
            params: Parameters to substitute
        Returns:
            Path to the compiled file
        '''
        if not os.path.isfile(prompt_file):
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")

        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read()

        compiled_content = self._substitute_parameters(content, params)

        base, ext = os.path.splitext(prompt_file)
        compiled_file = f"{base}.compiled{ext}"

        with open(compiled_file, 'w', encoding='utf-8') as f:
            f.write(compiled_content)

        return compiled_file

    def _substitute_parameters(self, content: str, params: Dict[str, str]) -> str:
        '''Substitute parameters in content.
        Args:
            content: Content to process
            params: Parameters to substitute
        Returns:
            Content with parameters substituted
        '''
        # Pattern matches {{param_name}}
        pattern = re.compile(r'\{\{(\w+)\}\}')

        def repl(match):
            key = match.group(1)
            return params.get(key, match.group(0))

        return pattern.sub(repl, content)
