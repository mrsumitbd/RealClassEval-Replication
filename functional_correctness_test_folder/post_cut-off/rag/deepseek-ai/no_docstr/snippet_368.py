
from typing import Dict
import re


class PromptCompiler:
    '''Compiles .prompt.md files with parameter substitution.'''

    def __init__(self):
        '''Initialize compiler.'''
        pass

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

        output_file = prompt_file.replace('.prompt.md', '.compiled.md')
        with open(output_file, 'w') as file:
            file.write(substituted_content)

        return output_file

    def _substitute_parameters(self, content: str, params: Dict[str, str]) -> str:
        '''Substitute parameters in content.
        Args:
            content: Content to process
            params: Parameters to substitute
        Returns:
            Content with parameters substituted
        '''
        for key, value in params.items():
            placeholder = f'{{{key}}}'
            content = content.replace(placeholder, value)
        return content
