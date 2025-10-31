
import os
import yaml
from typing import Dict, Optional, Tuple, List
from pathlib import Path


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

        # Execute the compiled command
        try:
            os.system(compiled_command)
            return True
        except Exception:
            return False

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
        config_path = Path('apm.yml')
        if not config_path.exists():
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
        compiled_command = command

        # Find all .prompt.md files in the current directory
        prompt_files = list(Path('.').glob('*.prompt.md'))

        for prompt_file in prompt_files:
            compiled_path = prompt_file.with_suffix('.txt')

            # Compile the prompt file if a compiler is provided
            if self.compiler:
                with open(prompt_file, 'r') as f:
                    content = f.read()
                compiled_content = self.compiler.compile(content, params)

                with open(compiled_path, 'w') as f:
                    f.write(compiled_content)

                compiled_files.append(str(compiled_path))
                compiled_command = self._transform_runtime_command(
                    compiled_command, str(
                        prompt_file), compiled_content, str(compiled_path)
                )

        return compiled_command, compiled_files

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
        # Replace the prompt file reference in the command with the compiled file path
        return command.replace(prompt_file, compiled_path)
