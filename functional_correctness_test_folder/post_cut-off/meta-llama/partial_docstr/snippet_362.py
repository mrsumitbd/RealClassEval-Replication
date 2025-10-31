
import os
import yaml
from typing import Dict, Optional, Tuple
import re


class ScriptRunner:

    def __init__(self, compiler=None):
        self.compiler = compiler
        self.config = self._load_config()

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        '''Run a script from apm.yml with parameter substitution.
        Args:
            script_name: Name of the script to run
            params: Parameters for compilation and script execution
        Returns:
            bool: True if script executed successfully
        '''
        if self.config is None or 'scripts' not in self.config:
            return False

        if script_name not in self.config['scripts']:
            return False

        command = self.config['scripts'][script_name]
        compiled_command, _ = self._auto_compile_prompts(command, params)

        for key, value in params.items():
            compiled_command = compiled_command.replace(f"${key}", value)

        try:
            os.system(compiled_command)
            return True
        except Exception as e:
            print(f"Error running script: {e}")
            return False

    def list_scripts(self) -> Dict[str, str]:
        if self.config is None or 'scripts' not in self.config:
            return {}

        return self.config['scripts']

    def _load_config(self) -> Optional[Dict]:
        try:
            with open('apm.yml', 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            return None

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> Tuple[str, list[str]]:
        '''Auto-compile .prompt.md files and transform runtime commands.
        Args:
            command: Original script command
            params: Parameters for compilation
        Returns:
            Tuple of (compiled_command, list_of_compiled_prompt_files)
        '''
        compiled_prompt_files = []
        prompt_files = re.findall(r'{(.*?)\.prompt\.md}', command)

        for prompt_file in prompt_files:
            prompt_file_path = f"{prompt_file}.prompt.md"
            if os.path.exists(prompt_file_path):
                with open(prompt_file_path, 'r') as file:
                    content = file.read()

                for key, value in params.items():
                    content = content.replace(f"${key}", value)

                compiled_path = f"{prompt_file}.compiled.md"
                with open(compiled_path, 'w') as file:
                    file.write(content)

                command = self._transform_runtime_command(
                    command, prompt_file, content, compiled_path)
                compiled_prompt_files.append(compiled_path)

        return command, compiled_prompt_files

    def _transform_runtime_command(self, command: str, prompt_file: str, compiled_content: str, compiled_path: str) -> str:
        return command.replace(f"{{{prompt_file}.prompt.md}}", compiled_content)
