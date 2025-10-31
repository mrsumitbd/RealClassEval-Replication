from typing import Dict, Optional
import re
from pathlib import Path
import subprocess
import yaml

class ScriptRunner:
    """Executes APM scripts with auto-compilation of .prompt.md files."""

    def __init__(self, compiler=None):
        """Initialize script runner with optional compiler."""
        self.compiler = compiler or PromptCompiler()

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        """Run a script from apm.yml with parameter substitution.

        Args:
            script_name: Name of the script to run
            params: Parameters for compilation and script execution

        Returns:
            bool: True if script executed successfully
        """
        config = self._load_config()
        if not config:
            raise RuntimeError('No apm.yml found in current directory')
        scripts = config.get('scripts', {})
        if script_name not in scripts:
            available = ', '.join(scripts.keys()) if scripts else 'none'
            raise RuntimeError(f"Script '{script_name}' not found. Available scripts: {available}")
        command = scripts[script_name]
        compiled_command, compiled_prompt_files = self._auto_compile_prompts(command, params)
        print(f'Executing: {compiled_command}')
        try:
            result = subprocess.run(compiled_command, shell=True, check=True)
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f'Script execution failed with exit code {e.returncode}')

    def list_scripts(self) -> Dict[str, str]:
        """List all available scripts from apm.yml.

        Returns:
            Dict mapping script names to their commands
        """
        config = self._load_config()
        return config.get('scripts', {}) if config else {}

    def _load_config(self) -> Optional[Dict]:
        """Load apm.yml from current directory."""
        config_path = Path('apm.yml')
        if not config_path.exists():
            return None
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> tuple[str, list[str]]:
        """Auto-compile .prompt.md files and transform runtime commands.

        Args:
            command: Original script command
            params: Parameters for compilation

        Returns:
            Tuple of (compiled_command, list_of_compiled_prompt_files)
        """
        prompt_files = re.findall('(\\S+\\.prompt\\.md)', command)
        compiled_prompt_files = []
        compiled_command = command
        for prompt_file in prompt_files:
            compiled_path = self.compiler.compile(prompt_file, params)
            compiled_prompt_files.append(prompt_file)
            with open(compiled_path, 'r') as f:
                compiled_content = f.read().strip()
            compiled_command = self._transform_runtime_command(compiled_command, prompt_file, compiled_content, compiled_path)
        return (compiled_command, compiled_prompt_files)

    def _transform_runtime_command(self, command: str, prompt_file: str, compiled_content: str, compiled_path: str) -> str:
        """Transform runtime commands to their proper execution format.

        Args:
            command: Original command
            prompt_file: Original .prompt.md file path
            compiled_content: Compiled prompt content as string
            compiled_path: Path to compiled .txt file

        Returns:
            Transformed command for proper runtime execution
        """
        if ' codex ' in command and re.search(re.escape(prompt_file), command):
            parts = command.split(' codex ', 1)
            potential_env_part = parts[0]
            codex_part = 'codex ' + parts[1]
            if '=' in potential_env_part and (not potential_env_part.startswith('codex')):
                env_vars = potential_env_part
                codex_match = re.search('codex\\s+(.*?)(' + re.escape(prompt_file) + ')(.*?)$', codex_part)
                if codex_match:
                    args_before_file = codex_match.group(1).strip()
                    args_after_file = codex_match.group(3).strip()
                    if args_before_file:
                        result = f"{env_vars} codex exec {args_before_file} '{compiled_content}'"
                    else:
                        result = f"{env_vars} codex exec '{compiled_content}'"
                    if args_after_file:
                        result += f' {args_after_file}'
                    return result
        elif re.search('codex\\s+.*' + re.escape(prompt_file), command):
            match = re.search('codex\\s+(.*?)(' + re.escape(prompt_file) + ')(.*?)$', command)
            if match:
                args_before_file = match.group(1).strip()
                args_after_file = match.group(3).strip()
                if args_before_file:
                    result = f"codex exec {args_before_file} '{compiled_content}'"
                else:
                    result = f"codex exec '{compiled_content}'"
                if args_after_file:
                    result += f' {args_after_file}'
                return result
        elif re.search('llm\\s+.*' + re.escape(prompt_file), command):
            match = re.search('llm\\s+(.*?)(' + re.escape(prompt_file) + ')(.*?)$', command)
            if match:
                args_before_file = match.group(1).strip()
                args_after_file = match.group(3).strip()
                result = f'llm'
                if args_before_file:
                    result += f' {args_before_file}'
                result += f" '{compiled_content}'"
                if args_after_file:
                    result += f' {args_after_file}'
                return result
        elif command.strip() == prompt_file:
            return f"codex exec '{compiled_content}'"
        return command.replace(prompt_file, compiled_path)