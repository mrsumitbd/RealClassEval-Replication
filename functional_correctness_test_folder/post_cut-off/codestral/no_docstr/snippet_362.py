
import os
import json
from typing import Dict, Optional, Tuple
import subprocess


class ScriptRunner:

    def __init__(self, compiler=None):
        self.compiler = compiler
        self.config = self._load_config()

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        if script_name not in self.list_scripts():
            return False

        script_path = self.list_scripts()[script_name]
        command = f"python {script_path}"

        if self.compiler:
            command, prompt_files = self._auto_compile_prompts(command, params)
            compiled_content = self.compiler.compile(prompt_files)
            compiled_path = os.path.join(os.path.dirname(
                script_path), "compiled_prompts.json")
            with open(compiled_path, 'w') as f:
                json.dump(compiled_content, f)
            command = self._transform_runtime_command(
                command, prompt_files[0], compiled_content, compiled_path)

        try:
            subprocess.run(command, shell=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def list_scripts(self) -> Dict[str, str]:
        scripts_dir = self.config.get("scripts_dir", "scripts")
        scripts = {}
        for filename in os.listdir(scripts_dir):
            if filename.endswith(".py"):
                script_name = filename[:-3]
                scripts[script_name] = os.path.join(scripts_dir, filename)
        return scripts

    def _load_config(self) -> Optional[Dict]:
        config_path = "config.json"
        if not os.path.exists(config_path):
            return None

        with open(config_path, 'r') as f:
            config = json.load(f)
        return config

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> Tuple[str, list[str]]:
        prompt_files = []
        for param_name, param_value in params.items():
            if param_name.startswith("prompt_"):
                prompt_files.append(param_value)

        if not prompt_files:
            return command, []

        compiled_command = command
        for prompt_file in prompt_files:
            compiled_command = compiled_command.replace(
                prompt_file, f"compiled_{os.path.basename(prompt_file)}")

        return compiled_command, prompt_files

    def _transform_runtime_command(self, command: str, prompt_file: str, compiled_content: str, compiled_path: str) -> str:
        compiled_command = command.replace(prompt_file, compiled_path)
        return compiled_command
