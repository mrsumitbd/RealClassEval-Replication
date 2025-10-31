
import os
import json
from typing import Dict, Optional
import subprocess


class ScriptRunner:
    '''Executes APM scripts with auto-compilation of .prompt.md files.'''

    def __init__(self, compiler=None):
        self.compiler = compiler if compiler else 'apm-promptc'
        self.config = self._load_config()
        self.scripts_dir = self.config.get(
            'scripts_dir', 'scripts') if self.config else 'scripts'

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        script_path = os.path.join(self.scripts_dir, script_name)
        if not os.path.exists(script_path):
            return False

        command = f'./{script_name}'
        command, params_list = self._auto_compile_prompts(command, params)

        try:
            subprocess.run([command] + params_list,
                           cwd=self.scripts_dir, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def list_scripts(self) -> Dict[str, str]:
        scripts = {}
        for filename in os.listdir(self.scripts_dir):
            if os.path.isfile(os.path.join(self.scripts_dir, filename)) and not filename.startswith('.'):
                scripts[filename] = os.path.join(self.scripts_dir, filename)
        return scripts

    def _load_config(self) -> Optional[Dict]:
        config_path = 'apm-scripts.json'
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return None

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> tuple[str, list[str]]:
        prompt_file = command.strip('./') + '.prompt.md'
        prompt_path = os.path.join(self.scripts_dir, prompt_file)

        if os.path.exists(prompt_path):
            compiled_path = prompt_path.replace('.prompt.md', '.promptc')
            if not os.path.exists(compiled_path) or os.path.getmtime(prompt_path) > os.path.getmtime(compiled_path):
                subprocess.run([self.compiler, prompt_path,
                               '-o', compiled_path], check=True)

            compiled_content = open(compiled_path, 'r').read()
            return self._transform_runtime_command(command, prompt_file, compiled_content, compiled_path), list(params.values())
        else:
            return command, list(params.values())

    def _transform_runtime_command(self, command: str, prompt_file: str, compiled_content: str, compiled_path: str) -> str:
        return f'{command} < {compiled_path}'
