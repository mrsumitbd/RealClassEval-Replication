from typing import Dict
import os
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
        if not os.path.isfile(prompt_file):
            raise FileNotFoundError(f'Prompt file not found: {prompt_file}')
        if not prompt_file.endswith('.prompt.md'):
            raise ValueError('Input file must have a .prompt.md extension.')

        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read()

        compiled_content = self._substitute_parameters(content, params)

        # remove '.prompt.md' and add '.md'
        out_path = prompt_file[:-10] + '.md'
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(compiled_content)

        return out_path

    def _substitute_parameters(self, content: str, params: Dict[str, str]) -> str:
        '''Substitute parameters in content.
        Args:
            content: Content to process
            params: Parameters to substitute
        Returns:
            Content with parameters substituted
        '''
        pattern = re.compile(r'\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}')

        def repl(match: re.Match) -> str:
            key = match.group(1)
            if key not in params:
                raise KeyError(f'Missing required parameter: {key}')
            val = params[key]
            return str(val)

        return pattern.sub(repl, content)
