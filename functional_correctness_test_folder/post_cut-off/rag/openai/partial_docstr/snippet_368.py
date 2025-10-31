
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

        # Build output path: replace .prompt.md with .compiled.md
        base, ext = os.path.splitext(prompt_file)
        if ext.lower() == '.md' and base.endswith('.prompt'):
            base = base[:-7]  # remove '.prompt'
        out_path = f"{base}.compiled.md"

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
        # Replace {{param}} and ${param} placeholders
        def repl(match):
            key = match.group(1)
            return params.get(key, match.group(0))

        # Handle {{param}}
        pattern_braces = re.compile(r'\{\{(\w+)\}\}')
        content = pattern_braces.sub(repl, content)

        # Handle ${param}
        pattern_dollar = re.compile(r'\$\{(\w+)\}')
        content = pattern_dollar.sub(repl, content)

        return content
