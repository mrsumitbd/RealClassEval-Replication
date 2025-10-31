
import os
import re
from typing import Dict, Optional, Tuple, List


class ScriptRunner:
    '''Executes APM scripts with auto-compilation of .prompt.md files.'''

    def __init__(self, compiler=None):
        self.compiler = compiler
        self.config = self._load_config()

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        if not self.config or script_name not in self.config.get('scripts', {}):
            return False

        script_info = self.config['scripts'][script_name]
        command = script_info.get('command', '')
        prompt_file = script_info.get('prompt_file', '')

        if prompt_file and prompt_file.endswith('.prompt.md'):
            command, compiled_paths = self._auto_compile_prompts(
                command, params)

        # Execute the command (placeholder for actual execution)
        print(f"Executing: {command}")
        return True

    def list_scripts(self) -> Dict[str, str]:
        if not self.config:
            return {}
        return {name: info.get('description', '') for name, info in self.config.get('scripts', {}).items()}

    def _load_config(self) -> Optional[Dict]:
        # Placeholder for actual config loading logic
        return {
            'scripts': {
                'example_script': {
                    'command': 'echo "Hello, World!"',
                    'prompt_file': 'example.prompt.md',
                    'description': 'An example script'
                }
            }
        }

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> Tuple[str, List[str]]:
        compiled_paths = []
        if not self.compiler:
            return command, compiled_paths

        # Placeholder for actual compilation logic
        prompt_file = 'example.prompt.md'
        compiled_content = f"Compiled content for {prompt_file}"
        compiled_path = f"compiled_{prompt_file.replace('.prompt.md', '.txt')}"

        with open(compiled_path, 'w') as f:
            f.write(compiled_content)

        compiled_paths.append(compiled_path)
        command = self._transform_runtime_command(
            command, prompt_file, compiled_content, compiled_path)
        return command, compiled_paths

    def _transform_runtime_command(self, command: str, prompt_file: str, compiled_content: str, compiled_path: str) -> str:
        # Placeholder for actual command transformation logic
        return command.replace(f"{{{prompt_file}}}", compiled_path)
