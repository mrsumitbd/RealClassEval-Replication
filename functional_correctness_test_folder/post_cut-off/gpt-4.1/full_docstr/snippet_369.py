
import os
import yaml
import re
from typing import Dict, Optional, List, Tuple


class ScriptRunner:
    '''Executes APM scripts with auto-compilation of .prompt.md files.'''

    def __init__(self, compiler=None):
        '''Initialize script runner with optional compiler.'''
        self.compiler = compiler or self._default_compiler
        self.config = self._load_config()

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        '''Run a script from apm.yml with parameter substitution.'''
        if not self.config or 'scripts' not in self.config:
            return False
        scripts = self.config['scripts']
        if script_name not in scripts:
            return False
        command = scripts[script_name]
        compiled_command, compiled_files = self._auto_compile_prompts(
            command, params)
        # Substitute params in command
        try:
            final_command = compiled_command.format(**params)
        except KeyError:
            return False
        # Actually run the command
        import subprocess
        try:
            result = subprocess.run(final_command, shell=True)
            return result.returncode == 0
        except Exception:
            return False

    def list_scripts(self) -> Dict[str, str]:
        '''List all available scripts from apm.yml.'''
        if not self.config or 'scripts' not in self.config:
            return {}
        return dict(self.config['scripts'])

    def _load_config(self) -> Optional[Dict]:
        '''Load apm.yml from current directory.'''
        apm_path = os.path.join(os.getcwd(), 'apm.yml')
        if not os.path.exists(apm_path):
            return None
        with open(apm_path, 'r', encoding='utf-8') as f:
            try:
                return yaml.safe_load(f)
            except Exception:
                return None

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> tuple[str, list[str]]:
        '''Auto-compile .prompt.md files and transform runtime commands.'''
        prompt_pattern = r'([^\s]+\.prompt\.md)'
        prompt_files = re.findall(prompt_pattern, command)
        compiled_files = []
        compiled_command = command
        for prompt_file in prompt_files:
            if not os.path.exists(prompt_file):
                continue
            with open(prompt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            compiled_content = self.compiler(content, params)
            compiled_path = prompt_file.replace('.prompt.md', '.txt')
            with open(compiled_path, 'w', encoding='utf-8') as f:
                f.write(compiled_content)
            compiled_files.append(compiled_path)
            compiled_command = self._transform_runtime_command(
                compiled_command, prompt_file, compiled_content, compiled_path
            )
        return compiled_command, compiled_files

    def _transform_runtime_command(self, command: str, prompt_file: str, compiled_content: str, compiled_path: str) -> str:
        '''Transform runtime commands to their proper execution format.'''
        # Replace the .prompt.md file with the .txt file in the command
        return command.replace(prompt_file, compiled_path)

    def _default_compiler(self, content: str, params: Dict[str, str]) -> str:
        # Simple param substitution: {param} in prompt file replaced by params['param']
        def replacer(match):
            key = match.group(1)
            return str(params.get(key, match.group(0)))
        return re.sub(r'\{(\w+)\}', replacer, content)
