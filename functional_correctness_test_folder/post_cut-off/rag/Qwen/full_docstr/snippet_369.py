
import os
import yaml
import re
from typing import Dict, Optional, List, Tuple
from jinja2 import Template


class ScriptRunner:
    '''Executes APM scripts with auto-compilation of .prompt.md files.'''

    def __init__(self, compiler=None):
        '''Initialize script runner with optional compiler.'''
        self.compiler = compiler or self._default_compiler
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
            print(f"Script '{script_name}' not found.")
            return False

        command = self.config['scripts'][script_name]
        compiled_command, compiled_files = self._auto_compile_prompts(
            command, params)
        try:
            os.system(compiled_command)
            return True
        except Exception as e:
            print(f"Failed to execute script '{script_name}': {e}")
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
        config_path = 'apm.yml'
        if not os.path.exists(config_path):
            print("apm.yml not found in the current directory.")
            return None

        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> Tuple[str, List[str]]:
        '''Auto-compile .prompt.md files and transform runtime commands.
        Args:
            command: Original script command
            params: Parameters for compilation
        Returns:
            Tuple of (compiled_command, list_of_compiled_prompt_files)
        '''
        compiled_files = []
        prompt_files = re.findall(
            r'{{\s*include\("([^"]+\.prompt\.md)"\)\s*}}', command)
        for prompt_file in prompt_files:
            with open(prompt_file, 'r') as file:
                content = file.read()
            compiled_content = self.compiler(content, params)
            compiled_path = prompt_file.replace('.prompt.md', '.compiled.txt')
            with open(compiled_path, 'w') as file:
                file.write(compiled_content)
            compiled_files.append(compiled_path)
            command = command.replace(
                f'{{{{ include("{prompt_file}") }}}}', compiled_path)

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
        # This method can be expanded based on specific transformation needs
        return command.replace(prompt_file, compiled_path)

    def _default_compiler(self, content: str, params: Dict[str, str]) -> str:
        '''Default compiler using Jinja2 templating.
        Args:
            content: Content of the .prompt.md file
            params: Parameters for compilation
        Returns:
            Compiled content as string
        '''
        template = Template(content)
        return template.render(params)
