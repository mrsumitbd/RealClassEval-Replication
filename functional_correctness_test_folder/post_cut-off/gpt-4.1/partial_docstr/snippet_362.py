
import os
import subprocess
import yaml
from typing import Dict, Optional, Tuple, List


class ScriptRunner:

    def __init__(self, compiler=None):
        self.compiler = compiler
        self.config = self._load_config()
        self.base_dir = os.getcwd()

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        if not self.config or 'scripts' not in self.config:
            return False
        scripts = self.config['scripts']
        if script_name not in scripts:
            return False
        command = scripts[script_name]
        # Compile prompts and transform command if needed
        compiled_command, compiled_prompts = self._auto_compile_prompts(
            command, params)
        # Substitute params in command
        try:
            final_command = compiled_command.format(**params)
        except KeyError:
            return False
        # Run the command
        try:
            result = subprocess.run(
                final_command, shell=True, cwd=self.base_dir)
            return result.returncode == 0
        except Exception:
            return False

    def list_scripts(self) -> Dict[str, str]:
        if not self.config or 'scripts' not in self.config:
            return {}
        return dict(self.config['scripts'])

    def _load_config(self) -> Optional[Dict]:
        config_path = os.path.join(self.base_dir, 'apm.yml')
        if not os.path.exists(config_path):
            return None
        with open(config_path, 'r', encoding='utf-8') as f:
            try:
                return yaml.safe_load(f)
            except Exception:
                return None

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> Tuple[str, List[str]]:
        import re
        prompt_pattern = re.compile(r'([^\s]+\.prompt\.md)')
        prompt_files = prompt_pattern.findall(command)
        compiled_files = []
        compiled_command = command
        for prompt_file in prompt_files:
            prompt_path = os.path.join(self.base_dir, prompt_file)
            if not os.path.exists(prompt_path):
                continue
            with open(prompt_path, 'r', encoding='utf-8') as f:
                content = f.read()
            try:
                compiled_content = content.format(**params)
            except Exception:
                compiled_content = content
            compiled_path = prompt_path.replace('.prompt.md', '.compiled.md')
            with open(compiled_path, 'w', encoding='utf-8') as f:
                f.write(compiled_content)
            compiled_files.append(compiled_path)
            # Transform command to use compiled prompt
            compiled_command = self._transform_runtime_command(
                compiled_command, prompt_file, compiled_content, compiled_path
            )
        return compiled_command, compiled_files

    def _transform_runtime_command(self, command: str, prompt_file: str, compiled_content: str, compiled_path: str) -> str:
        # Replace the prompt_file in the command with compiled_path
        return command.replace(prompt_file, compiled_path)
