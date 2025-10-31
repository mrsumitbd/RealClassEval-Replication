
import os
import yaml
from typing import Dict, Optional, Tuple
import re


class ScriptRunner:
    '''Executes APM scripts with auto-compilation of .prompt.md files.'''

    def __init__(self, compiler=None):
        '''Initialize script runner with optional compiler.'''
        self.compiler = compiler if compiler else self._default_compile

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        '''Run a script from apm.yml with parameter substitution.
        Args:
            script_name: Name of the script to run
            params: Parameters for compilation and script execution
        Returns:
            bool: True if script executed successfully
        '''
        config = self._load_config()
        if config and 'scripts' in config:
            scripts = config['scripts']
            if script_name in scripts:
                command = scripts[script_name]
                compiled_command, _ = self._auto_compile_prompts(
                    command, params)
                # Replace params in command
                for key, value in params.items():
                    compiled_command = compiled_command.replace(
                        f"${key}", value)
                try:
                    os.system(compiled_command)
                    return True
                except Exception as e:
                    print(f"Error running script: {e}")
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
        try:
            with open('apm.yml', 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print("apm.yml not found in current directory.")
        except yaml.YAMLError as e:
            print(f"Error parsing apm.yml: {e}")
        return None

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> Tuple[str, list[str]]:
        '''Auto-compile .prompt.md files and transform runtime commands.
        Args:
            command: Original script command
            params: Parameters for compilation
        Returns:
            Tuple of (compiled_command, list_of_compiled_prompt_files)
        '''
        compiled_files = []
        prompt_files = re.findall(r'(\S+\.prompt\.md)', command)
        for prompt_file in prompt_files:
            compiled_path = prompt_file.replace('.prompt.md', '.txt')
            with open(prompt_file, 'r') as file:
                content = file.read()
                for key, value in params.items():
                    content = content.replace(f"${key}", value)
                compiled_content = self.compiler(content)
            with open(compiled_path, 'w') as compiled_file:
                compiled_file.write(compiled_content)
            command = self._transform_runtime_command(
                command, prompt_file, compiled_content, compiled_path)
            compiled_files.append(compiled_path)
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
        # Simple transformation: replace .prompt.md with .txt
        return command.replace(prompt_file, compiled_path)

    @staticmethod
    def _default_compile(content: str) -> str:
        # For demonstration, just return the content as is
        return content
