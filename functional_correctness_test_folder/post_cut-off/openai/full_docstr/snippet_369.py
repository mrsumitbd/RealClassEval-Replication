
import os
import re
import subprocess
import yaml
from typing import Dict, List, Optional, Tuple


class ScriptRunner:
    '''Executes APM scripts with auto-compilation of .prompt.md files.'''

    def __init__(self, compiler=None):
        '''Initialize script runner with optional compiler.'''
        self.compiler = compiler  # unused in this minimal implementation

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        '''Run a script from apm.yml with parameter substitution.
        Args:
            script_name: Name of the script to run
            params: Parameters for compilation and script execution
        Returns:
            bool: True if script executed successfully
        '''
        config = self._load_config()
        if not config or 'scripts' not in config:
            return False

        scripts = config['scripts']
        if script_name not in scripts:
            return False

        command = scripts[script_name]
        # Substitute parameters in the command string
        try:
            command = command.format(**params)
        except KeyError:
            # Missing parameter
            return False

        # Auto‑compile any .prompt.md files referenced in the command
        command, compiled_files = self._auto_compile_prompts(command, params)

        # Execute the final command
        try:
            result = subprocess.run(command, shell=True, check=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            return result.returncode == 0
        except subprocess.CalledProcessError:
            return False

    def list_scripts(self) -> Dict[str, str]:
        '''List all available scripts from apm.yml.
        Returns:
            Dict mapping script names to their commands
        '''
        config = self._load_config()
        if not config or 'scripts' not in config:
            return {}
        return config['scripts']

    def _load_config(self) -> Optional[Dict]:
        '''Load apm.yml from current directory.'''
        path = os.path.join(os.getcwd(), 'apm.yml')
        if not os.path.isfile(path):
            return None
        with open(path, 'r', encoding='utf-8') as f:
            try:
                return yaml.safe_load(f)
            except yaml.YAMLError:
                return None

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> Tuple[str, List[str]]:
        '''Auto-compile .prompt.md files and transform runtime commands.
        Args:
            command: Original script command
            params: Parameters for compilation
        Returns:
            Tuple of (compiled_command, list_of_compiled_prompt_files)
        '''
        prompt_pattern = re.compile(r'([^\s]+\.prompt\.md)')
        matches = prompt_pattern.findall(command)
        compiled_files = []

        for prompt_path in matches:
            if not os.path.isfile(prompt_path):
                continue
            with open(prompt_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Simple placeholder replacement: {{param}}
            compiled_content = re.sub(r'\{\{(\w+)\}\}',
                                      lambda m: params.get(m.group(1), ''),
                                      content)

            compiled_path = os.path.splitext(prompt_path)[0] + '.txt'
            with open(compiled_path, 'w', encoding='utf-8') as f:
                f.write(compiled_content)

            compiled_files.append(compiled_path)

            # Transform the command to use the compiled file
            command = self._transform_runtime_command(command,
                                                      prompt_path,
                                                      compiled_content,
                                                      compiled_path)

        return command, compiled_files

    def _transform_runtime_command(self, command: str, prompt_file: str,
                                   compiled_content: str, compiled_path: str) -> str:
        '''Transform runtime commands to their proper execution format.
        Args:
            command: Original command
            prompt_file: Original .prompt.md file path
            compiled_content: Compiled prompt content as string
            compiled_path: Path to compiled .txt file
        Returns:
            Transformed command for proper runtime execution
        '''
        # Replace the original prompt file reference with the compiled path
        return command.replace(prompt_file, compiled_path)
