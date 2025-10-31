
import os
import yaml
import subprocess
from typing import Dict, Optional, List, Tuple


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
            result = subprocess.run(compiled_command, shell=True, check=True)
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
        return dict(config['scripts'])

    def _load_config(self) -> Optional[Dict]:
        '''Load apm.yml from current directory.'''
        if self._config is not None:
            return self._config
        apm_path = os.path.join(os.getcwd(), 'apm.yml')
        if not os.path.exists(apm_path):
            return None
        with open(apm_path, 'r', encoding='utf-8') as f:
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
        import re

        prompt_pattern = r'([^\s]+\.prompt\.md)'
        prompt_files = re.findall(prompt_pattern, command)
        compiled_files = []
        compiled_command = command

        for prompt_file in prompt_files:
            if not os.path.exists(prompt_file):
                continue
            with open(prompt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            # Simple param substitution: {{param}}
            for k, v in params.items():
                content = content.replace('{{' + k + '}}', str(v))
            compiled_path = prompt_file.replace('.prompt.md', '.txt')
            with open(compiled_path, 'w', encoding='utf-8') as f:
                f.write(content)
            compiled_files.append(compiled_path)
            compiled_command = self._transform_runtime_command(
                compiled_command, prompt_file, content, compiled_path
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
        # Replace the .prompt.md file reference with the compiled .txt file in the command
        return command.replace(prompt_file, compiled_path)
