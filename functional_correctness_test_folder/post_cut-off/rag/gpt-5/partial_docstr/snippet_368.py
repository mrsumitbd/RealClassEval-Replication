import os
import re
from typing import Dict


class PromptCompiler:
    '''Compiles .prompt.md files with parameter substitution.'''

    def __init__(self):
        '''Initialize compiler.'''
        self._pattern = re.compile(
            r'\{\{\s*([A-Za-z_][A-Za-z0-9_\-\.]*)\s*\}\}')

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
        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read()

        compiled_content = self._substitute_parameters(content, params)

        if prompt_file.endswith('.prompt.md'):
            out_path = prompt_file[:-len('.prompt.md')] + '.md'
        else:
            base, ext = os.path.splitext(prompt_file)
            if ext.lower() == '.md' and base.endswith('.prompt'):
                out_path = base[:-len('.prompt')] + '.md'
            else:
                out_path = f'{prompt_file}.compiled.md'

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
        placeholders = {m.group(1) for m in self._pattern.finditer(content)}
        missing = [key for key in placeholders if key not in params]
        if missing:
            raise ValueError(
                f'Missing parameters for placeholders: {", ".join(sorted(missing))}')

        def repl(match: re.Match) -> str:
            key = match.group(1)
            return str(params.get(key, ''))

        return self._pattern.sub(repl, content)
