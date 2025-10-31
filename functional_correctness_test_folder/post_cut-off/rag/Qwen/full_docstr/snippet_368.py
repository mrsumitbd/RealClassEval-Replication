
from typing import Dict


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
            Compiled content with parameters substituted
        '''
        with open(prompt_file, 'r') as file:
            content = file.read()
        return self._substitute_parameters(content, params)

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
