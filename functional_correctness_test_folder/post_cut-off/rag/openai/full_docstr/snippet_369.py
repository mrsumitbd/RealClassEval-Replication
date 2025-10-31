
import os
import re
import subprocess
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ScriptRunner:
    """Executes APM scripts with auto‑compilation of .prompt.md files."""

    def __init__(self, compiler=None):
        """
        Initialize script runner with optional compiler.

        Parameters
        ----------
        compiler : object, optional
            An object that provides a ``compile(file_path: str) -> str`` method
            which returns the compiled content of a ``.prompt.md`` file.
        """
        self.compiler = compiler

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        """
        Run a script from apm.yml with parameter substitution.

        Parameters
        ----------
        script_name : str
            Name of the script to run.
        params : Dict[str, str]
            Parameters for compilation and script execution.

        Returns
        -------
        bool
            True if script executed successfully, False otherwise.
        """
        config = self._load_config()
        if not config:
            raise FileNotFoundError("apm.yml not found in current directory")

        scripts = config.get("scripts", {})
        if script_name not in scripts:
            raise KeyError(f"Script '{script_name}' not found in apm.yml")

        # Substitute parameters in the command string
        command = scripts[script_name].format(**params)

        # Auto‑compile any .prompt.md files referenced in the command
        compiled_command, compiled_files = self._auto_compile_prompts(
            command, params)

        # Execute the compiled command
        try:
            result = subprocess.run(
                compiled_command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
            )
            # Optionally, you could log result.stdout / result.stderr here
            return True
        except subprocess.CalledProcessError as exc:
            # You might want to log exc.stdout / exc.stderr
            return False

    def list_scripts(self) -> Dict[str, str]:
        """
        List all available scripts from apm.yml.

        Returns
        -------
        Dict[str, str]
            Mapping of script names to their command strings.
        """
        config = self._load_config()
        if not config:
            return {}
        return config.get("scripts", {})

    def _load_config(self) -> Optional[Dict]:
        """
        Load apm.yml from current directory.

        Returns
        -------
        Optional[Dict]
            Parsed YAML content or None if file does not exist.
        """
        config_path = Path.cwd() / "apm.yml"
        if not config_path.is_file():
            return None
        with config_path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def _auto_compile_prompts(
        self, command: str, params: Dict[str, str]
    ) -> Tuple[str, List[str]]:
        """
        Auto‑compile .prompt.md files and transform runtime commands.

        Parameters
        ----------
        command : str
            Original script command.
        params : Dict[str, str]
            Parameters for compilation.

        Returns
        -------
        Tuple[str, List[str]]
            Compiled command string and list of compiled prompt file paths.
        """
        prompt_pattern = re.compile(r"([^\s]+\.prompt\.md)")
        compiled_files: List[str] = []

        def _compile_file(prompt_path: str) -> str:
            """Compile a single .prompt.md file to .txt."""
            prompt_file = Path(prompt_path)
            if not prompt_file.is_file():
                raise FileNotFoundError(
                    f"Prompt file not found: {prompt_path}")

            # Determine compiled path
            compiled_path = prompt_file.with_suffix(".txt")

            # Compile content
            if self.compiler and hasattr(self.compiler, "compile"):
                compiled_content = self.compiler.compile(str(prompt_file))
            else:
                # Default: copy content as-is
                compiled_content = prompt_file.read_text(encoding="utf-8")

            # Write compiled content
            compiled_path.write_text(compiled_content, encoding="utf-8")
            compiled_files.append(str(compiled_path))
            return str(compiled_path)

        # Find all .prompt.md references and replace them
        def _replace_match(match: re.Match) -> str:
            original = match.group(1)
            compiled = _compile_file(original)
            return compiled

        compiled_command = prompt_pattern.sub(_replace_match, command)
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

        Parameters
        ----------
        command : str
            Original command.
        prompt_file : str
            Original .prompt.md file path.
        compiled_content : str
            Compiled prompt content as string.
        compiled_path : str
            Path to compiled .txt file.

        Returns
        -------
        str
            Transformed command for proper runtime execution.
        """
        # In this simplified implementation, we just replace the prompt file
        # reference with the compiled path.  The compiled content is not used
        # directly in the command string.
        return command.replace(prompt_file, compiled_path)
