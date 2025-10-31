
import yaml
from typing import Dict, Optional, Tuple
import os
import re
import subprocess
from pathlib import Path


class ScriptRunner:
    '''Executes APM scripts with auto-compilation of .prompt.md files.'''

    def __init__(self, compiler=None):
        '''Initialize script runner with optional compiler.'''
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
        if not config or 'scripts' not in config or script_name not in config['scripts']:
            return False

        command = config['scripts'][script_name]
        compiled_command, compiled_files = self._auto_compile_prompts(
            command, params)

        try:
            subprocess.run(compiled_command, shell=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def list_scripts(self) -> Dict[str, str]:
        '''List all available scripts from apm.yml.
        Returns:
            Dict mapping script names to their commands
        '''
        config = self._load_config()
        return config.get('scripts', {}) if config else {}

    def _load_config(self) -> Optional[Dict]:
        '''Load apm.yml from current directory.'''
        if self._config is None:
            config_path = Path('apm.yml')
            if not config_path.exists():
                return None
            with open(config_path, 'r') as f:
                self._config = yaml.safe_load(f)
        return self._config

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> Tuple[str, list[str]]:
        '''Auto-compile .prompt.md files and transform runtime commands.
        Args:
            command: Original script command
            params: Parameters for compilation
        Returns:
            Tuple of (compiled_command, list_of_compiled_prompt_files)
        '''
        compiled_files = []
        current_command = command

        # Find all .prompt.md files in the command
        prompt_files = re.findall(r'(\S+\.prompt\.md)', command)

        for prompt_file in prompt_files:
            if not os.path.exists(prompt_file):
                continue

            with open(prompt_file, 'r') as f:
                prompt_content = f.read()

            # Compile the prompt content (replace placeholders with params)
            compiled_content = prompt_content
            for key, value in params.items():
                compiled_content = compiled_content.replace(
                    f'{{{key}}}', value)

            # Write compiled content to .txt file
            compiled_path = prompt_file.replace('.prompt.md', '.txt')
            with open(compiled_path, 'w') as f:
                f.write(compiled_content)

            compiled_files.append(compiled_path)

            # Transform the command to use the compiled file
            current_command = self._transform_runtime_command(
                current_command, prompt_file, compiled_content, compiled_path
            )

        return current_command, compiled_files

    def _transform_runtime_command(self, command: str, prompt_file: str, compiled_content: str, compiled_path: str) -> str:
        '''Transform runtime commands to their proper execution format.
        Args:
            command: Original command
            prompt_file: Original .prompt.md file path
            compiled_content: Compiled prompt content as string
            compiled_path: Path to compiled .txt file
        Returns:
            Transformed command for proper runtime execution
        '''
        return command.replace(prompt_file, compiled_path)
