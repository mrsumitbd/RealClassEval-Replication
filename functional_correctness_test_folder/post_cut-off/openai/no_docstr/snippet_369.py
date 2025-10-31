
import os
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Optional, Tuple, List


class ScriptRunner:
    """
    A simple script runner that can list available Python scripts,
    automatically compile prompt files referenced in a command string,
    transform the command for runtime execution, and run the script
    with supplied parameters.
    """

    def __init__(self, compiler=None):
        """
        Initialize the ScriptRunner.

        Parameters
        ----------
        compiler : callable, optional
            A callable that accepts a prompt file path and returns
            the compiled content as a string. If None, the raw
            content of the prompt file is used.
        """
        self.compiler = compiler
        self.script_dir = Path(__file__).parent / "scripts"
        self.config_path = Path(__file__).parent / "config.json"

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        """
        Run a script by name with the given parameters.

        Parameters
        ----------
        script_name : str
            The name of the script (without extension) to run.
        params : Dict[str, str]
            A dictionary of parameters to pass to the script as
            command‑line arguments.

        Returns
        -------
        bool
            True if the script executed successfully (exit code 0),
            False otherwise.
        """
        scripts = self.list_scripts()
        if script_name not in scripts:
            raise FileNotFoundError(f"Script '{script_name}' not found.")

        script_path = scripts[script_name]
        # Build the base command
        cmd = ["python", str(script_path)]

        # Add parameters as --key value
        for key, value in params.items():
            cmd.extend([f"--{key}", value])

        # Auto‑compile any prompts referenced in the command
        cmd_str = " ".join(cmd)
        cmd_str, compiled_files = self._auto_compile_prompts(cmd_str, params)

        # Transform the command for runtime (currently a no‑op)
        cmd_str = self._transform_runtime_command(
            cmd_str, compiled_files[0] if compiled_files else "", "", ""
        )

        # Execute the command
        try:
            result = subprocess.run(
                cmd_str.split(),
                check=True,
                capture_output=True,
                text=True,
            )
            # Optionally, you could log result.stdout / result.stderr
            return result.returncode == 0
        except subprocess.CalledProcessError:
            return False

    def list_scripts(self) -> Dict[str, str]:
        """
        List all Python scripts in the scripts directory.

        Returns
        -------
        Dict[str, str]
            A mapping from script name (without extension) to its full path.
        """
        scripts = {}
        if not self.script_dir.exists():
            return scripts
        for file in self.script_dir.iterdir():
            if file.suffix == ".py":
                scripts[file.stem] = str(file.resolve())
        return scripts

    def _load_config(self) -> Optional[Dict]:
        """
        Load configuration from config.json if it exists.

        Returns
        -------
        Optional[Dict]
            The configuration dictionary or None if the file does not exist.
        """
        if not self.config_path.exists():
            return None
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _auto_compile_prompts(
        self, command: str, params: Dict[str, str]
    ) -> Tuple[str, List[str]]:
        """
        Detect prompt file references in the command string, compile them,
        and replace the references with the paths to the compiled files.

        Parameters
        ----------
        command : str
            The command string that may contain prompt references.
        params : Dict[str, str]
            Parameters that may be used for prompt compilation.

        Returns
        -------
        Tuple[str, List[str]]
            The updated command string and a list of compiled file paths.
        """
        compiled_files = []
        # Simple pattern: look for "prompt:<path>"
        parts = command.split()
        new_parts = []
        for part in parts:
            if part.startswith("prompt:"):
                prompt_path = part[len("prompt:"):]
                prompt_file = Path(prompt_path)
                if not prompt_file.is_absolute():
                    prompt_file = Path(__file__).parent / prompt_file
                if not prompt_file.exists():
                    raise FileNotFoundError(
                        f"Prompt file '{prompt_file}' not found.")
                # Read the prompt content
                with open(prompt_file, "r", encoding="utf-8") as pf:
                    content = pf.read()
                # Compile if a compiler is provided
                if self.compiler:
                    compiled_content = self.compiler(content, **params)
                else:
                    compiled_content = content
                # Write to a temporary file
                tmp = tempfile.NamedTemporaryFile(
                    mode="w", delete=False, suffix=".txt", encoding="utf-8"
                )
                tmp.write(compiled_content)
                tmp.close()
                compiled_files.append(tmp.name)
                new_parts.append(tmp.name)
            else:
                new_parts.append(part)
        new_command = " ".join(new_parts)
        return new_command, compiled_files

    def _transform_runtime_command(
        self,
        command: str,
        prompt_file: str,
        compiled_content: str,
        compiled_path: str,
    ) -> str:
        """
        Transform the command string for runtime execution.
        Currently this is a placeholder that simply returns the command.

        Parameters
        ----------
        command : str
            The command string to transform.
        prompt_file : str
            The original
