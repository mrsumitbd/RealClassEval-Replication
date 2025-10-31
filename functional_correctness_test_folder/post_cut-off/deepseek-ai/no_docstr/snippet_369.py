
from typing import Dict, Optional, Tuple
import os
import subprocess
import json
from pathlib import Path


class ScriptRunner:

    def __init__(self, compiler=None):
        self.compiler = compiler
        self.config = self._load_config()

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        if not self.config or script_name not in self.config.get("scripts", {}):
            return False

        script_info = self.config["scripts"][script_name]
        command = script_info.get("command", "")
        prompt_file = script_info.get("prompt_file", "")

        if not command:
            return False

        compiled_command, compiled_paths = self._auto_compile_prompts(
            command, params)
        if prompt_file:
            compiled_content = ""
            for path in compiled_paths:
                if os.path.exists(path):
                    with open(path, "r") as f:
                        compiled_content += f.read()

            compiled_command = self._transform_runtime_command(
                compiled_command, prompt_file, compiled_content, compiled_paths[
                    0] if compiled_paths else ""
            )

        try:
            subprocess.run(compiled_command, shell=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def list_scripts(self) -> Dict[str, str]:
        if not self.config:
            return {}
        return {name: info.get("description", "") for name, info in self.config.get("scripts", {}).items()}

    def _load_config(self) -> Optional[Dict]:
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        if not os.path.exists(config_path):
            return None

        with open(config_path, "r") as f:
            return json.load(f)

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> Tuple[str, list[str]]:
        if not self.compiler:
            return command, []

        compiled_paths = []
        for param, value in params.items():
            output_path = f"compiled_{param}.txt"
            self.compiler.compile(value, output_path)
            compiled_paths.append(output_path)

        return command, compiled_paths

    def _transform_runtime_command(self, command: str, prompt_file: str, compiled_content: str, compiled_path: str) -> str:
        if not compiled_content:
            return command

        temp_prompt_path = "temp_prompt.txt"
        with open(temp_prompt_path, "w") as f:
            f.write(compiled_content)

        transformed_command = command.replace(
            f"{{{prompt_file}}}", temp_prompt_path)
        return transformed_command
