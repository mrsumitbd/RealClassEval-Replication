from typing import Dict
import os
import re


class PromptCompiler:
    '''Compiles .prompt.md files with parameter substitution.'''

    def __init__(self):
        '''Initialize compiler.'''
        self._pattern = re.compile(r"\{\{\s*([A-Za-z0-9_.-]+)\s*\}\}")

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

        with open(prompt_file, "r", encoding="utf-8") as f:
            content = f.read()

        compiled_content = self._substitute_parameters(content, params)

        if prompt_file.endswith(".prompt.md"):
            compiled_path = prompt_file[:-10] + ".compiled.md"
        else:
            base, ext = os.path.splitext(prompt_file)
            compiled_path = f"{base}.compiled{ext or '.md'}"

        with open(compiled_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(compiled_content)

        return compiled_path

    def _substitute_parameters(self, content: str, params: Dict[str, str]) -> str:
        '''Substitute parameters in content.
        Args:
            content: Content to process
            params: Parameters to substitute
        Returns:
            Content with parameters substituted
        '''
        def repl(match: re.Match) -> str:
            key = match.group(1)
            if key in params and params[key] is not None:
                return str(params[key])
            return match.group(0)

        return self._pattern.sub(repl, content)
