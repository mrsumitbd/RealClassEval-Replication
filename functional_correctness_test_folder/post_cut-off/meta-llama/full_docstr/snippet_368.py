
import re
from typing import Dict
import os
import uuid


class PromptCompiler:
    '''Compiles .prompt.md files with parameter substitution.'''

    def __init__(self):
        '''Initialize compiler.'''
        self._temp_dir = './temp'

        # Create the temp directory if it doesn't exist
        if not os.path.exists(self._temp_dir):
            os.makedirs(self._temp_dir)

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

        compiled_content = self._substitute_parameters(content, params)

        # Generate a unique filename for the compiled file
        filename = os.path.basename(prompt_file)
        compiled_filename = f"{uuid.uuid4()}_{filename.replace('.prompt.md', '.md')}"
        compiled_file_path = os.path.join(self._temp_dir, compiled_filename)

        with open(compiled_file_path, 'w') as file:
            file.write(compiled_content)

        return compiled_file_path

    def _substitute_parameters(self, content: str, params: Dict[str, str]) -> str:
        '''Substitute parameters in content.
        Args:
            content: Content to process
            params: Parameters to substitute
        Returns:
            Content with parameters substituted
        '''
        pattern = r'\{\{(.*?)\}\}'

        def replace(match):
            param_name = match.group(1).strip()
            return params.get(param_name, match.group(0))

        return re.sub(pattern, replace, content)
