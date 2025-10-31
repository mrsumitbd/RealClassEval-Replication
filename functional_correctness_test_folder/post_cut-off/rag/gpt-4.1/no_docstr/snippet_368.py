import os
import re
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
            Path to the compiled file
        '''
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        substituted = self._substitute_parameters(content, params)
        base, ext = os.path.splitext(prompt_file)
        compiled_file = base + '.compiled' + ext
        with open(compiled_file, 'w', encoding='utf-8') as f:
            f.write(substituted)
        return compiled_file

    def _substitute_parameters(self, content: str, params: Dict[str, str]) -> str:
        '''Substitute parameters in content.
        Args:
            content: Content to process
            params: Parameters to substitute
        Returns:
            Content with parameters substituted
        '''
        def replacer(match):
            key = match.group(1)
            return params.get(key, match.group(0))
        pattern = re.compile(r'\{\{(\w+)\}\}')
        return pattern.sub(replacer, content)
