
import yaml
import os
from typing import Dict, Optional, Tuple, List
import subprocess
import re


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
        if not self.config or script_name not in self.config['scripts']:
            return False

        command = self.config['scripts'][script_name]
        compiled_command, compiled_files = self._auto_compile_prompts(
            command, params)

        try:
            result = subprocess.run(compiled_command, shell=True, check=True)
            return result.returncode == 0
        except subprocess.CalledProcessError:
            return False
        finally:
            for file in compiled_files:
                if os.path.exists(file):
                    os.remove(file)

    def list_scripts(self) -> Dict[str, str]:
        '''List all available scripts from apm.yml.
        Returns:
            Dict mapping script names to their commands
        '''
        return self.config.get('scripts', {}) if self.config else {}

    def _load_config(self) -> Optional[Dict]:
        '''Load apm.yml from current directory.'''
        config_path = 'apm.yml'
        if not os.path.exists(config_path):
            return None

        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> Tuple[str, List[str]]:
        '''Auto-compile .prompt.md files and transform runtime commands.
        Args:
            command: Original script command
            params: Parameters for compilation
        Returns:
            Tuple of (compiled_command, list_of_compiled_prompt_files)
        '''
        compiled_files = []
        prompt_files = re.findall(r'\{([^}]+\.prompt\.md)\}', command)

        for prompt_file in prompt_files:
            if not os.path.exists(prompt_file):
                continue

            with open(prompt_file, 'r') as f:
                content = f.read()

            compiled_content = self.compiler.compile(
                content, params) if self.compiler else content
            compiled_path = prompt_file.replace('.prompt.md', '.txt')

            with open(compiled_path, 'w') as f:
                f.write(compiled_content)

            compiled_files.append(compiled_path)
            command = command.replace(f'{{{prompt_file}}}', compiled_path)

        return command, compiled_files

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
        if '{prompt_file}' in command:
            command = command.replace('{prompt_file}', compiled_path)
        return command
