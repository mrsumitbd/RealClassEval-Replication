
import os
import re
import subprocess
import yaml
from typing import Dict, Optional, Tuple, List


class ScriptRunner:
    '''Executes APM scripts with auto-compilation of .prompt.md files.'''

    def __init__(self, compiler=None):
        '''Initialize script runner with optional compiler.'''
        self.compiler = compiler
        self._config = self._load_config()

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        '''Run a script from apm.yml with parameter substitution.
        Args:
            script_name: Name of the script to run
            params: Parameters for compilation and script execution
        Returns:
            bool: True if script executed successfully
        '''
        if not self._config:
            return False

        scripts = self._config.get('scripts', {})
        if script_name not in scripts:
            return False

        command = scripts[script_name]
        # Substitute simple placeholders in the command
        for key, value in params.items():
            command = command.replace(f'{{{{{key}}}}}', value)

        # Auto‑compile any .prompt.md files referenced in the command
        command, compiled_files = self._auto_compile_prompts(command, params)

        # Transform runtime command if needed
        for prompt_file, compiled_path in compiled_files:
            command = self._transform_runtime_command(
                command, prompt_file, compiled_path, compiled_path
            )

        # Execute the final command
        try:
            result = subprocess.run(
                command, shell=True, check=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            return result.returncode == 0
        except subprocess.CalledProcessError:
            return False

    def list_scripts(self) -> Dict[str, str]:
        '''List all available scripts from apm.yml.
        Returns:
            Dict mapping script names to their commands
        '''
        if not self._config:
            return {}
        return self._config.get('scripts', {})

    def _load_config(self) -> Optional[Dict]:
        '''Load apm.yml from current directory.'''
        config_path = os.path.join(os.getcwd(), 'apm.yml')
        if not os.path.isfile(config_path):
            return None
        with open(config_path, 'r', encoding='utf-8') as f:
            try:
                return yaml.safe_load(f)
            except yaml.YAMLError:
                return None

    def _auto_compile_prompts(
        self, command: str, params: Dict[str, str]
    ) -> Tuple[str, List[Tuple[str, str]]]:
        '''Auto-compile .prompt.md files and transform runtime commands.
        Args:
            command: Original script command
            params: Parameters for compilation
        Returns:
            Tuple of (compiled_command, list_of_compiled_prompt_files)
        '''
        prompt_pattern = re.compile(r'([^\s]+\.prompt\.md)')
        compiled_files: List[Tuple[str, str]] = []

        def replace_match(match):
            prompt_path = match.group(1)
            if not os.path.isabs(prompt_path):
                prompt_path = os.path.join(os.getcwd(), prompt_path)
            if not os.path.isfile(prompt_path):
                return prompt_path  # leave unchanged if file missing

            # Read and compile the prompt
            with open(prompt_path, 'r', encoding='utf-8') as pf:
                content = pf.read()
            for key, value in params.items():
                content = content.replace(f'{{{{{key}}}}}', value)

            # Write compiled content to .txt file
            compiled_path = os.path.splitext(prompt_path)[0] + '.txt'
            with open(compiled_path, 'w', encoding='utf-8') as cf:
                cf.write(content)

            compiled_files.append((prompt_path, compiled_path))
            return compiled_path

        new_command = prompt_pattern.sub(replace_match, command)
        return new_command, compiled_files

    def _transform_runtime_command(
        self, command: str, prompt_file: str, compiled_content: str, compiled_path: str
    ) -> str:
        '''Transform runtime commands to their proper execution format.
        Args:
            command: Original command
            prompt_file: Original .prompt.md file path
            compiled_content: Compiled prompt content as string
            compiled_path: Path to compiled .txt file
        Returns:
            Transformed command for proper runtime execution
        '''
        # In this simplified implementation we just return the command unchanged.
        # The placeholder replacement is already handled in _auto_compile_prompts.
        return command
