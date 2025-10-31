
import os
import json
from typing import Dict, Optional
import subprocess


class ScriptRunner:

    def __init__(self, compiler=None):
        self.compiler = compiler
        self.config = self._load_config()
        self.scripts_dir = self.config.get(
            'scripts_dir', 'scripts') if self.config else 'scripts'

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        script_path = os.path.join(self.scripts_dir, script_name)
        if not os.path.exists(script_path):
            return False

        command, args = self._auto_compile_prompts(script_name, params)
        if self.compiler:
            compiled_path = os.path.join(
                self.scripts_dir, f'{script_name}.compiled')
            with open(compiled_path, 'w') as f:
                subprocess.run([self.compiler, script_path], stdout=f)
            command = self._transform_runtime_command(
                command, script_name, compiled_path, compiled_path)
            script_path = compiled_path

        try:
            subprocess.run([command, *args], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def list_scripts(self) -> Dict[str, str]:
        scripts = {}
        for filename in os.listdir(self.scripts_dir):
            filepath = os.path.join(self.scripts_dir, filename)
            if os.path.isfile(filepath):
                scripts[filename] = filepath
        return scripts

    def _load_config(self) -> Optional[Dict]:
        config_path = 'config.json'
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return None

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> tuple[str, list[str]]:
        args = []
        for key, value in params.items():
            args.append(f'--{key}')
            args.append(value)
        return command, args

    def _transform_runtime_command(self, command: str, prompt_file: str, compiled_content: str, compiled_path: str) -> str:
        return command
