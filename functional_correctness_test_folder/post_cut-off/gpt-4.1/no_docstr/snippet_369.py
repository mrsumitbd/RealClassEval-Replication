
import os
import json
from typing import Dict, Optional


class ScriptRunner:

    def __init__(self, compiler=None):
        self.compiler = compiler
        self.scripts_dir = "scripts"
        self.config_path = os.path.join(self.scripts_dir, "config.json")
        self._config = None

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        scripts = self.list_scripts()
        if script_name not in scripts:
            return False
        script_path = scripts[script_name]
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()
        if self.compiler:
            compiled_content = self.compiler(content, params)
        else:
            compiled_content = content.format(**params)
        compiled_path = script_path + ".compiled"
        with open(compiled_path, "w", encoding="utf-8") as f:
            f.write(compiled_content)
        command = self._config.get("commands", {}).get(
            script_name, f"python {compiled_path}")
        runtime_command = self._transform_runtime_command(
            command, script_path, compiled_content, compiled_path)
        exit_code = os.system(runtime_command)
        return exit_code == 0

    def list_scripts(self) -> Dict[str, str]:
        scripts = {}
        if not os.path.isdir(self.scripts_dir):
            return scripts
        for fname in os.listdir(self.scripts_dir):
            if fname.endswith(".py") or fname.endswith(".sh"):
                scripts[fname] = os.path.join(self.scripts_dir, fname)
        return scripts

    def _load_config(self) -> Optional[Dict]:
        if self._config is not None:
            return self._config
        if not os.path.exists(self.config_path):
            self._config = {}
            return self._config
        with open(self.config_path, "r", encoding="utf-8") as f:
            self._config = json.load(f)
        return self._config

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> tuple[str, list[str]]:
        prompts = []
        for k, v in params.items():
            prompt = f"--{k}={v}"
            prompts.append(prompt)
        new_command = command + " " + " ".join(prompts)
        return new_command, prompts

    def _transform_runtime_command(self, command: str, prompt_file: str, compiled_content: str, compiled_path: str) -> str:
        cmd = command.replace("{prompt_file}", prompt_file)
        cmd = cmd.replace("{compiled_path}", compiled_path)
        return cmd
