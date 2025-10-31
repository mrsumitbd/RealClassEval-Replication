
import os
from typing import Dict


class PromptCompiler:
    '''Compiles .prompt.md files with parameter substitution.'''

    def __init__(self):
        '''Initialize compiler.'''
        self.compiled_dir = 'compiled_prompts'
        os.makedirs(self.compiled_dir, exist_ok=True)

    def compile(self, prompt_file: str, params: Dict[str, str]) -> str:
        '''Compile a .prompt.md file with parameter substitution.
        Args:
            prompt_file: Path to the .prompt.md file
            params: Parameters to substitute
        Returns:
            Path to the compiled file
        '''
        with open(prompt_file, 'r') as file:
            content = file.read()

        substituted_content = self._substitute_parameters(content, params)

        compiled_file = os.path.join(
            self.compiled_dir, os.path.basename(prompt_file))
        with open(compiled_file, 'w') as file:
            file.write(substituted_content)

        return compiled_file

    def _substitute_parameters(self, content: str, params: Dict[str, str]) -> str:
        '''Substitute parameters in content.
        Args:
            content: Content to process
            params: Parameters to substitute
        Returns:
            Content with parameters substituted
        '''
        for key, value in params.items():
            content = content.replace(f'{{{key}}}', value)
        return content
