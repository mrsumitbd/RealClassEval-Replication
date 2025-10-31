
import os
import json
from typing import Dict, Optional, Tuple, List
import subprocess


class ScriptRunner:
    '''Executes APM scripts with auto-compilation of .prompt.md files.'''

    def __init__(self, compiler=None):
        self.compiler = compiler
        self.config = self._load_config()

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        scripts = self.list_scripts()
        if script_name not in scripts:
            return False

        script_path = scripts[script_name]
        command = f"apm run {script_path}"

        if script_path.endswith('.prompt.md'):
            command, _ = self._auto_compile_prompts(command, params)

        try:
            subprocess.run(command, shell=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def list_scripts(self) -> Dict[str, str]:
        scripts = {}
        for root, _, files in os.walk('.'):
            for file in files:
                if file.endswith('.apm') or file.endswith('.prompt.md'):
                    script_name = os.path.splitext(file)[0]
                    scripts[script_name] = os.path.join(root, file)
        return scripts

    def _load_config(self) -> Optional[Dict]:
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                return json.load(f)
        return None

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> Tuple[str, List[str]]:
        prompt_file = command.split()[-1]
        compiled_content = self.compiler.compile(prompt_file, params)
        compiled_path = os.path.splitext(prompt_file)[0] + '.apm'
        command = self._transform_runtime_command(
            command, prompt_file, compiled_content, compiled_path)
        return command, [compiled_path]

    def _transform_runtime_command(self, command: str, prompt_file: str, compiled_content: str, compiled_path: str) -> str:
        with open(compiled_path, 'w') as f:
            f.write(compiled_content)
        return command.replace(prompt_file, compiled_path)
