
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
        compiler : Callable[[str, Dict[str, str]], str] | None
            A function that takes a prompt file path and a params dict and
            returns the compiled prompt content as a string.  If ``None`` a
            very small default compiler that simply returns the file
            contents unchanged is used.
        """
        if compiler is None:

            def default_compiler(prompt_path: str, params: Dict[str, str]) -> str:
                with open(prompt_path, "r", encoding="utf-8") as f:
                    return f.read()

            self.compiler = default_compiler
        else:
            self.compiler = compiler

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
            raise FileNotFoundError("apm.yml not found in current directory")

        scripts = config.get("scripts", {})
        if script_name not in scripts:
            raise KeyError(f"Script '{script_name}' not found in apm.yml")

        # Substitute parameters in the command string
        raw_command = scripts[script_name]
        command = raw_command.format(**params)

        # Auto‑compile any .prompt.md files referenced in the command
        compiled_command, compiled_files = self._auto_compile_prompts(
            command, params)

        # Execute the compiled command
        try:
            result = subprocess.run(
                compiled_command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
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
            Mapping of script names to their raw command strings.
        """
        config = self._load_config()
        if not config:
            return {}
        return config.get("scripts", {})

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _load_config(self) -> Optional[Dict]:
        """
        Load apm.yml from current directory.

        Returns
        -------
        Optional[Dict]
            Parsed YAML content or ``None`` if the file does not exist.
        """
        config_path = Path.cwd() / "apm.yml"
        if not config_path.is_file():
            return None
        with open(config_path, "r", encoding="utf-8") as f:
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
        compiled_files: List[str] = []

        # Find all .prompt.md references in the command
        prompt_paths = re.findall(r"([^\s]+\.prompt\.md)", command)
        for prompt_path in prompt_paths:
            prompt_file = Path(prompt_path)
            if not prompt_file.is_file():
                continue  # skip if file does not exist

            # Compile the prompt
            compiled_content = self.compiler(str(prompt_file), params)

            # Write compiled content to a .txt file in the same directory
            compiled_path = prompt_file.with_suffix(".txt")
            with open(compiled_path, "w", encoding="utf-8") as f:
                f.write(compiled_content)

            compiled_files.append(str(compiled_path))

            # Replace the original .prompt.md reference with the compiled .txt path
            command = command.replace(str(prompt_file), str(compiled_path))

        # After compilation, transform any runtime commands if needed
        command = self._transform_runtime_command(command, compiled_files)

        return command, compiled_files

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
            Original command after prompt compilation.
        compiled_files : List[str]
            List of compiled prompt file paths.

        Returns
        -------
        str
            Transformed command for proper runtime execution.
        """
        # This is a placeholder for any additional transformations that
        # might be required by the runtime environment.  For now we simply
        # return the command unchanged.
        return command
