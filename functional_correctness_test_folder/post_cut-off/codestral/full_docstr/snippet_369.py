
import os
import yaml
from typing import Dict, Optional, Tuple
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
        compiled_command, compiled_prompts = self._auto_compile_prompts(
            command, params)

        # Execute the compiled command
        # Placeholder for actual execution logic
        # For example: os.system(compiled_command)
        return True

    def list_scripts(self) -> Dict[str, str]:
        '''List all available scripts from apm.yml.
        Returns:
            Dict mapping script names to their commands
        '''
        if not self.config:
            return {}
        return self.config.get('scripts', {})

    def _load_config(self) -> Optional[Dict]:
        '''Load apm.yml from current directory.'''
        if not os.path.exists('apm.yml'):
            return None

        with open('apm.yml', 'r') as file:
            return yaml.safe_load(file)

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> Tuple[str, list[str]]:
        '''Auto-compile .prompt.md files and transform runtime commands.
        Args:
            command: Original script command
            params: Parameters for compilation
        Returns:
            Tuple of (compiled_command, list_of_compiled_prompt_files)
        '''
        compiled_prompts = []
        prompt_files = re.findall(r'\{([^}]+\.prompt\.md)\}', command)

        for prompt_file in prompt_files:
            if not os.path.exists(prompt_file):
                continue

            compiled_content = self.compiler.compile(prompt_file, params)
            compiled_path = prompt_file.replace('.prompt.md', '.txt')

            with open(compiled_path, 'w') as file:
                file.write(compiled_content)

            compiled_prompts.append(compiled_path)
            command = self._transform_runtime_command(
                command, prompt_file, compiled_content, compiled_path)

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
        # Replace the prompt file placeholder with the compiled path
        command = command.replace(f'{{{prompt_file}}}', compiled_path)
        return command
