
import os
import re
import subprocess
import yaml
from pathlib import Path
from typing import Dict, Optional, Tuple, List, Any


class ScriptRunner:
    """Executes APM scripts with auto‑compilation of .prompt.md files."""

    def __init__(self, compiler: Optional[Any] = None):
        """
        Initialize script runner with optional compiler.

        Parameters
        ----------
        compiler : Any, optional
            An object that implements a ``compile`` method accepting a
            ``prompt_file`` path and a ``params`` mapping and returning the
            compiled content as a string.  If ``None`` a very small default
            compiler is used that simply copies the file contents to a
            ``.txt`` file.
        """
        self.compiler = compiler or self._default_compiler

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
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
            ``True`` if the script executed successfully, ``False`` otherwise.
        """
        config = self._load_config()
        if not config:
            print("No apm.yml found in the current directory.")
            return False

        scripts = config.get("scripts", {})
        if script_name not in scripts:
            print(f"Script '{script_name}' not found in apm.yml.")
            return False

        # 1. Substitute parameters in the command string
        command = scripts[script_name]
        command = self._substitute_params(command, params)

        # 2. Auto‑compile any referenced .prompt.md files
        command, compiled_files = self._auto_compile_prompts(command, params)

        # 3. Transform runtime command if needed
        command = self._transform_runtime_command(command, compiled_files)

        # 4. Execute the command
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as exc:
            print(f"Command failed with exit code {exc.returncode}")
            print(exc.stderr)
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

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _load_config(self) -> Optional[Dict]:
        """Load apm.yml from current directory."""
        path = Path.cwd() / "apm.yml"
        if not path.is_file():
            return None
        try:
            with path.open("r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception as exc:
            print(f"Failed to load apm.yml: {exc}")
            return None

    def _substitute_params(self, command: str, params: Dict[str, str]) -> str:
        """Replace placeholders in the command with provided parameters."""
        # Simple placeholder patterns: {{key}} or ${key}
        for key, value in params.items():
            command = command.replace(f"{{{{{key}}}}}", value)
            command = command.replace(f"${key}", value)
        return command

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
            Compiled command and list of compiled prompt file paths.
        """
        prompt_pattern = re.compile(r"([^\s]+\.prompt\.md)")
        compiled_files: List[str] = []

        def _compile_and_replace(match: re.Match) -> str:
            prompt_path = match.group(1)
            prompt_file = Path(prompt_path)
            if not prompt_file.is_file():
                print(
                    f"Prompt file {prompt_path} not found; skipping compilation.")
                return prompt_path

            # Compile the prompt
            compiled_content = self.compiler.compile(str(prompt_file), params)
            compiled_path = prompt_file.with_suffix(".txt")
            compiled_path.write_text(compiled_content, encoding="utf-8")
            compiled_files.append(str(compiled_path))
            return str(compiled_path)

        new_command = prompt_pattern.sub(_compile_and_replace, command)
        return new_command, compiled_files

    def _transform_runtime_command(
        self,
        command: str,
        compiled_files: List[str],
    ) -> str:
        """
        Transform runtime commands to their proper execution format.

        Parameters
        ----------
        command : str
            Original command.
        compiled_files : List[str]
            List of compiled prompt file paths.

        Returns
        -------
        str
            Transformed command for proper runtime execution.
        """
        # In this simplified implementation we do not modify the command.
        # The method is kept for compatibility with the original design.
        return command

    # ------------------------------------------------------------------
    # Default compiler
    # ------------------------------------------------------------------
    class _default_compiler:
        @staticmethod
        def compile(prompt_file: str, params: Dict[str, str]) -> str:
            """
            Default compiler that simply copies the prompt file content
            to a .txt file, performing the same parameter substitution
            as the command substitution.

            Parameters
            ----------
            prompt_file : str
                Path to the .prompt.md file.
            params : Dict[str, str]
                Parameters for substitution.

            Returns
            -------
            str
                Compiled content.
            """
            content = Path(prompt_file).read_text(encoding="utf-8")
            for key, value in params.items():
                content = content.replace(f"{{{{{key}}}}}", value)
                content = content.replace(f"${key}", value)
            return content
