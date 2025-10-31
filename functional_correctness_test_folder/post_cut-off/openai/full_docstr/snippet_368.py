
import re
from pathlib import Path
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
        src_path = Path(prompt_file)
        if not src_path.is_file():
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")

        # Read original content
        content = src_path.read_text(encoding="utf-8")

        # Substitute parameters
        compiled_content = self._substitute_parameters(content, params)

        # Determine output file path: replace .prompt.md with .compiled.md
        if src_path.suffixes[-2:] == ['.prompt', '.md']:
            # e.g., example.prompt.md -> example.compiled.md
            base = src_path.with_suffix('')  # removes .md
            base = base.with_suffix('')      # removes .prompt
            out_path = base.with_name(base.name + ".compiled.md")
        else:
            # fallback: just add .compiled before .md
            out_path = src_path.with_name(src_path.stem + ".compiled.md")

        # Write compiled content
        out_path.write_text(compiled_content, encoding="utf-8")

        return str(out_path)

    def _substitute_parameters(self, content: str, params: Dict[str, str]) -> str:
        '''Substitute parameters in content.
        Args:
            content: Content to process
            params: Parameters to substitute
        Returns:
            Content with parameters substituted
        '''
        # Replace {{param}} with the corresponding value from params
        pattern = re.compile(r'\{\{(\w+)\}\}')

        def repl(match):
            key = match.group(1)
            return params.get(key, match.group(0))

        return pattern.sub(repl, content)
