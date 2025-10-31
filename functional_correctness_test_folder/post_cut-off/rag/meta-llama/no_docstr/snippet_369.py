
import os
import yaml
from typing import Dict, Optional, List
import re
import subprocess
from jinja2 import Template


class ScriptRunner:
    '''Executes APM scripts with auto-compilation of .prompt.md files.'''

    def __init__(self, compiler=None):
        '''Initialize script runner with optional compiler.'''
        self.compiler = compiler
        self.config = self._load_config()

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        '''Run a script from apm.yml with parameter substitution.
        Args:
            script_name: Name of the script to run
            params: Parameters for compilation and script execution
        Returns:
            bool: True if script executed successfully
        '''
        if not self.config or 'scripts' not in self.config or script_name not in self.config['scripts']:
            return False

        command = self.config['scripts'][script_name]
        compiled_command, compiled_prompts = self._auto_compile_prompts(
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
        if not self.config or 'scripts' not in self.config:
            return {}

        return self.config['scripts']

    def _load_config(self) -> Optional[Dict]:
        '''Load apm.yml from current directory.'''
        config_path = os.path.join(os.getcwd(), 'apm.yml')
        if not os.path.exists(config_path):
            return None

        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> tuple[str, List[str]]:
        '''Auto-compile .prompt.md files and transform runtime commands.
        Args:
            command: Original script command
            params: Parameters for compilation
        Returns:
            Tuple of (compiled_command, list_of_compiled_prompt_files)
        '''
        prompt_files = re.findall(r'\{(.*?)\.prompt\.md\}', command)
        compiled_prompts = []

        for prompt_file in prompt_files:
            compiled_path = f'{prompt_file}.txt'
            with open(f'{prompt_file}.prompt.md', 'r') as f:
                template = Template(f.read())
                compiled_content = template.render(**params)

            with open(compiled_path, 'w') as f:
                f.write(compiled_content)

            compiled_prompts.append(compiled_path)
            command = command.replace(
                f'{{{prompt_file}.prompt.md}}', compiled_path)

        return command, compiled_prompts

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
        # This method is not used in the provided implementation,
        # but it's kept here as it's part of the class definition.
        return command.replace(f'{{{prompt_file}}}', compiled_path)
