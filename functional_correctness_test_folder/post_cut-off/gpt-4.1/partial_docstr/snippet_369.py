
import os
import glob
import json
from typing import Dict, Optional, List


class ScriptRunner:
    '''Executes APM scripts with auto-compilation of .prompt.md files.'''

    def __init__(self, compiler=None):
        self.compiler = compiler
        self.scripts_dir = os.path.abspath("scripts")
        self.prompts_dir = os.path.abspath("prompts")
        self.compiled_dir = os.path.abspath("compiled_prompts")
        os.makedirs(self.compiled_dir, exist_ok=True)
        self.config = self._load_config()

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        scripts = self.list_scripts()
        if script_name not in scripts:
            return False
        command = scripts[script_name]
        command, compiled_files = self._auto_compile_prompts(command, params)
        # Simulate running the command (in real use, subprocess would be used)
        # For this implementation, just return True if command is non-empty
        return bool(command)

    def list_scripts(self) -> Dict[str, str]:
        scripts = {}
        scripts_path = os.path.join(self.scripts_dir, "*.json")
        for script_file in glob.glob(scripts_path):
            with open(script_file, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, dict):
                        scripts.update(data)
                except Exception:
                    continue
        return scripts

    def _load_config(self) -> Optional[Dict]:
        config_path = os.path.join(self.scripts_dir, "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return None
        return None

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> tuple[str, List[str]]:
        import re
        prompt_pattern = re.compile(r"\{prompt:([^\}]+)\}")
        compiled_files = []

        def compile_prompt(prompt_file):
            prompt_path = os.path.join(self.prompts_dir, prompt_file)
            compiled_path = os.path.join(
                self.compiled_dir, prompt_file.replace('.prompt.md', '.compiled.txt'))
            if not os.path.exists(prompt_path):
                return None, None
            with open(prompt_path, "r", encoding="utf-8") as f:
                content = f.read()
            # Simple param replacement
            for k, v in params.items():
                content = content.replace("{{" + k + "}}", v)
            if self.compiler:
                compiled_content = self.compiler(content)
            else:
                compiled_content = content
            with open(compiled_path, "w", encoding="utf-8") as f:
                f.write(compiled_content)
            compiled_files.append(compiled_path)
            return compiled_content, compiled_path

        def repl(match):
            prompt_file = match.group(1)
            compiled_content, compiled_path = compile_prompt(prompt_file)
            if compiled_content is None:
                return match.group(0)
            return self._transform_runtime_command(match.group(0), prompt_file, compiled_content, compiled_path)

        new_command = prompt_pattern.sub(repl, command)
        return new_command, compiled_files

    def _transform_runtime_command(self, command: str, prompt_file: str, compiled_content: str, compiled_path: str) -> str:
        # Replace the {prompt:...} with the path to the compiled file
        return compiled_path
