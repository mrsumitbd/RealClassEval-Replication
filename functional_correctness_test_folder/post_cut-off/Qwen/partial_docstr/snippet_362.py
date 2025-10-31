
from typing import Dict, Optional, List, Tuple
import os
import yaml
import re


class ScriptRunner:

    def __init__(self, compiler=None):
        self.compiler = compiler
        self.config = self._load_config()

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        if not self.config or script_name not in self.config['scripts']:
            return False

        script_info = self.config['scripts'][script_name]
        command = script_info['command']

        compiled_command, compiled_prompt_files = self._auto_compile_prompts(
            command, params)

        try:
            os.system(compiled_command)
            return True
        except Exception as e:
            print(f"Error executing script: {e}")
            return False

    def list_scripts(self) -> Dict[str, str]:
        if not self.config:
            return {}
        return {name: info['description'] for name, info in self.config['scripts'].items()}

    def _load_config(self) -> Optional[Dict]:
        try:
            with open('apm.yml', 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print("Configuration file 'apm.yml' not found.")
            return None
        except yaml.YAMLError as exc:
            print(f"Error in configuration file: {exc}")
            return None

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> Tuple[str, List[str]]:
        compiled_prompt_files = []
        for key, value in params.items():
            if key.endswith('.prompt.md'):
                compiled_content = self.compiler.compile(value)
                compiled_path = f"compiled_{key}"
                with open(compiled_path, 'w') as file:
                    file.write(compiled_content)
                compiled_prompt_files.append(compiled_path)
                command = self._transform_runtime_command(
                    command, key, compiled_content, compiled_path)
        return command, compiled_prompt_files

    def _transform_runtime_command(self, command: str, prompt_file: str, compiled_content: str, compiled_path: str) -> str:
        placeholder = f"{{{prompt_file}}}"
        return command.replace(placeholder, compiled_path)
