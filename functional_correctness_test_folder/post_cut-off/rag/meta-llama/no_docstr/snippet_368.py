
import re
from typing import Dict
import os
import tempfile


class PromptCompiler:
    """Compiles .prompt.md files with parameter substitution."""

    def __init__(self):
        """Initialize compiler."""
        pass

    def compile(self, prompt_file: str, params: Dict[str, str]) -> str:
        """Compile a .prompt.md file with parameter substitution.

        Args:
            prompt_file: Path to the .prompt.md file
            params: Parameters to substitute

        Returns:
            Path to the compiled file
        """
        with open(prompt_file, 'r') as infile:
            content = infile.read()
        compiled_content = self._substitute_parameters(content, params)

        # Create a temporary file with the same name but without the .prompt suffix
        filename = os.path.basename(prompt_file)
        if filename.endswith('.prompt.md'):
            filename = filename[:-9] + '.md'
        else:
            filename += '.compiled'

        tmp_file = tempfile.NamedTemporaryFile(
            mode='w', delete=False, prefix='prompt_compiler_', suffix=filename)
        tmp_file.write(compiled_content)
        tmp_file.close()

        return tmp_file.name

    def _substitute_parameters(self, content: str, params: Dict[str, str]) -> str:
        """Substitute parameters in content.

        Args:
            content: Content to process
            params: Parameters to substitute

        Returns:
            Content with parameters substituted
        """
        def replace(match):
            param_name = match.group(1)
            return params.get(param_name, match.group(0))

        pattern = r'\{\{\s*(\w+)\s*\}\}'
        return re.sub(pattern, replace, content)
