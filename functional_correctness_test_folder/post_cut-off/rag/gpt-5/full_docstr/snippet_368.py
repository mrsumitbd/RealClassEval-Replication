from typing import Dict
import os
import re


class PromptCompiler:
    '''Compiles .prompt.md files with parameter substitution.'''

    def __init__(self):
        '''Initialize compiler.'''
        self._placeholder_regex = re.compile(
            r"\{\{\s*([A-Za-z_][A-Za-z0-9_\-\.]*)\s*\}\}")

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
            out_path = prompt_file + '.compiled.md'

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
        placeholders = {m.group(1)
                        for m in self._placeholder_regex.finditer(content)}
        missing = sorted(k for k in placeholders if k not in params)
        if missing:
            raise ValueError(
                f'Missing parameters for placeholders: {", ".join(missing)}')

        def repl(match: re.Match) -> str:
            key = match.group(1)
            value = params.get(key, '')
            if not isinstance(value, str):
                value = str(value)
            return value

        return self._placeholder_regex.sub(repl, content)
