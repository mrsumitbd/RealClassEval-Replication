
from typing import Dict, Optional, Tuple, List
import subprocess
import yaml
import os
import re


class ScriptRunner:

    def __init__(self, compiler=None):
        self.compiler = compiler
        self._config = None

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        '''Run a script from apm.yml with parameter substitution.
        Args:
            script_name: Name of the script to run
            params: Parameters for compilation and script execution
        Returns:
            bool: True if script executed successfully
        '''
        config = self._load_config()
        if config is None or 'scripts' not in config:
            return False

        scripts = config['scripts']
        if script_name not in scripts:
            return False

        command = scripts[script_name]
        compiled_command, compiled_files = self._auto_compile_prompts(
            command, params)

        try:
            # Substitute parameters in the command
            for key, value in params.items():
                compiled_command = compiled_command.replace(
                    f'{{{key}}}', value)

            # Run the command
            result = subprocess.run(compiled_command, shell=True, check=True)
            return result.returncode == 0
        except subprocess.CalledProcessError:
            return False
        finally:
            # Clean up compiled files if any
            for file in compiled_files:
                if os.path.exists(file):
                    os.remove(file)

    def list_scripts(self) -> Dict[str, str]:
        config = self._load_config()
        if config is None or 'scripts' not in config:
            return {}
        return config['scripts']

    def _load_config(self) -> Optional[Dict]:
        if self._config is not None:
            return self._config

        config_path = 'apm.yml'
        if not os.path.exists(config_path):
            return None

        with open(config_path, 'r') as f:
            self._config = yaml.safe_load(f)

        return self._config

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> Tuple[str, List[str]]:
        '''Auto-compile .prompt.md files and transform runtime commands.
        Args:
            command: Original script command
            params: Parameters for compilation
        Returns:
            Tuple of (compiled_command, list_of_compiled_prompt_files)
        '''
        if self.compiler is None:
            return command, []

        prompt_files = re.findall(r'(\S+\.prompt\.md)', command)
        compiled_files = []
        compiled_command = command

        for prompt_file in prompt_files:
            if not os.path.exists(prompt_file):
                continue

            with open(prompt_file, 'r') as f:
                content = f.read()

            compiled_content = self.compiler.compile(content, params)
            compiled_path = prompt_file.replace('.prompt.md', '.compiled.md')

            with open(compiled_path, 'w') as f:
                f.write(compiled_content)

            compiled_files.append(compiled_path)
            compiled_command = self._transform_runtime_command(
                compiled_command, prompt_file, compiled_content, compiled_path
            )

        return compiled_command, compiled_files

    def _transform_runtime_command(self, command: str, prompt_file: str, compiled_content: str, compiled_path: str) -> str:
        return command.replace(prompt_file, compiled_path)
