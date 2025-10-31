
import os
import re
import subprocess
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Callable


class ScriptRunner:
    """Executes APM scripts with auto‑compilation of .prompt.md files."""

    def __init__(self, compiler: Optional[Callable[[Path, Dict[str, str]], str]] = None):
        """
        Initialize script runner with optional compiler.

        :param compiler: A callable that receives a Path to a .prompt.md file and a
                         dictionary of parameters, and returns the compiled
                         content as a string. If None, a default compiler that
                         performs simple placeholder substitution is used.
        """
        self.compiler = compiler or self._default_compiler

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        """
        Run a script from apm.yml with parameter substitution.

        :param script_name: Name of the script to run
        :param params: Parameters for compilation and script execution
        :return: True if script executed successfully
        """
        config = self._load_config()
        if not config:
            return False

        scripts = config.get("scripts", {})
        if script_name not in scripts:
            return False

        command = scripts[script_name]
        # Parameter substitution
        command = re.sub(
            r"\{\{(\w+)\}\}",
            lambda m: str(params.get(m.group(1), "")),
            command,
        )

        compiled_command, _ = self._auto_compile_prompts(command, params)

        try:
            result = subprocess.run(
                compiled_command,
                shell=True,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                # Log error output if needed
                return False
            return True
        except Exception:
            return False

    def list_scripts(self) -> Dict[str, str]:
        """
        List all available scripts from apm.yml.

        :return: Dict mapping script names to their commands
        """
        config = self._load_config()
        if not config:
            return {}
        return config.get("scripts", {})

    def _load_config(self) -> Optional[Dict]:
        """Load apm.yml from current directory."""
        config_path = Path.cwd() / "apm.yml"
        if not config_path.is_file():
            return None
        try:
            with config_path.open("r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return None

    def _auto_compile_prompts(
        self, command: str, params: Dict[str, str]
    ) -> Tuple[str, List[str]]:
        """
        Auto‑compile .prompt.md files and transform runtime commands.

        :param command: Original script command
        :param params: Parameters for compilation
        :return: Tuple of (compiled_command, list_of_compiled_prompt_files)
        """
        prompt_pattern = re.compile(r"([^\s]+\.prompt\.md)")
        compiled_files: List[str] = []

        def replace_match(match: re.Match) -> str:
            prompt_path = Path(match.group(1))
            if not prompt_path.is_file():
                # If the file does not exist, leave the original path
                return str(prompt_path)

            compiled_content = self.compiler(prompt_path, params)
            compiled_path = prompt_path.with_suffix(".txt")
            try:
                compiled_path.write_text(compiled_content, encoding="utf-8")
                compiled_files.append(str(compiled_path))
                return str(compiled_path)
            except Exception:
                # If writing fails, keep original
                return str(prompt_path)

        compiled_command = prompt_pattern.sub(replace_match, command)
        return compiled_command, compiled_files

    def _transform_runtime_command(
        self,
        command: str,
        prompt_file: str,
        compiled_content: str,
        compiled_path: str,
    ) -> str:
        """
        Transform runtime commands to their proper execution format.

        :param command: Original command
        :param prompt_file: Original .prompt.md file path
        :param compiled_content: Compiled prompt content as string
        :param compiled_path: Path to compiled .txt file
        :return: Transformed command for proper runtime execution
        """
        # Write compiled content to file
        try:
            Path(compiled_path).write_text(compiled_content, encoding="utf-8")
        except Exception:
            pass
        # Replace the prompt file reference in the command
        return command.replace(prompt_file, compiled_path)

    @staticmethod
    def _default_compiler(prompt_path: Path, params: Dict[str, str]) -> str:
        """
        Default compiler that performs simple placeholder substitution.

        :param prompt_path: Path to the .prompt.md file
        :param params: Parameters for substitution
        :return: Compiled content as string
        """
        try:
            content = prompt_path.read_text(encoding="utf-8")
        except Exception:
            return ""

        # Replace {{param}} placeholders with provided values
        def repl(match: re.Match) -> str:
            key = match.group(1)
            return str(params.get(key, ""))

        return re.sub(r"\{\{(\w+)\}\}", repl, content)
