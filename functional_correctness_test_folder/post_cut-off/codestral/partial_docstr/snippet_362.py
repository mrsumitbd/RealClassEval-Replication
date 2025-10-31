
import os
import yaml
from typing import Dict, Optional, Tuple
import subprocess


class ScriptRunner:

    def __init__(self, compiler=None):
        self.compiler = compiler
        self.config = self._load_config()

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        if script_name not in self.config['scripts']:
            raise ValueError(f"Script {script_name} not found in config")

        script_config = self.config['scripts'][script_name]
        command = script_config['command']

        if 'prompts' in script_config:
            command, compiled_prompts = self._auto_compile_prompts(
                command, params)
        else:
            compiled_prompts = []

        try:
            subprocess.run(command, shell=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def list_scripts(self) -> Dict[str, str]:
        return {name: config['description'] for name, config in self.config['scripts'].items()}

    def _load_config(self) -> Optional[Dict]:
        config_path = 'apm.yml'
        if not os.path.exists(config_path):
            return None

        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> Tuple[str, list[str]]:
        compiled_prompts = []
        for prompt_file in self.config['prompts']:
            compiled_content, compiled_path = self.compiler.compile(
                prompt_file, params)
            command = self._transform_runtime_command(
                command, prompt_file, compiled_content, compiled_path)
            compiled_prompts.append(compiled_path)

        return command, compiled_prompts

    def _transform_runtime_command(self, command: str, prompt_file: str, compiled_content: str, compiled_path: str) -> str:
        return command.replace(f'<{prompt_file}>', compiled_path)
