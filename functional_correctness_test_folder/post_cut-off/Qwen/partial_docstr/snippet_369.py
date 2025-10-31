
from typing import Dict, Optional, List
import os
import json
import subprocess


class ScriptRunner:
    '''Executes APM scripts with auto-compilation of .prompt.md files.'''

    def __init__(self, compiler=None):
        self.compiler = compiler or 'default_compiler'
        self.config = self._load_config()

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        command = self.config.get(script_name)
        if not command:
            print(f"Script {script_name} not found.")
            return False
        prompt_file, dependencies = self._auto_compile_prompts(command, params)
        transformed_command = self._transform_runtime_command(
            command, prompt_file, dependencies[0], dependencies[1])
        try:
            subprocess.run(transformed_command, shell=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def list_scripts(self) -> Dict[str, str]:
        return self.config or {}

    def _load_config(self) -> Optional[Dict]:
        try:
            with open('config.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return None

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> tuple[str, List[str]]:
        prompt_file = command.split()[0]
        compiled_content = self._compile_prompt(prompt_file, params)
        compiled_path = f"{prompt_file}.compiled"
        with open(compiled_path, 'w') as file:
            file.write(compiled_content)
        return prompt_file, [compiled_content, compiled_path]

    def _transform_runtime_command(self, command: str, prompt_file: str, compiled_content: str, compiled_path: str) -> str:
        return command.replace(prompt_file, compiled_path)

    def _compile_prompt(self, prompt_file: str, params: Dict[str, str]) -> str:
        with open(prompt_file, 'r') as file:
            content = file.read()
        for key, value in params.items():
            content = content.replace(f"{{{key}}}", value)
        return content
