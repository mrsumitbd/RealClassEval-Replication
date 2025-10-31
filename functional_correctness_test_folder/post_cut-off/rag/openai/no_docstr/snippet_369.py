
import os
import re
import subprocess
import yaml
from pathlib import Path
from typing import Dict, Optional, Tuple, List


class ScriptRunner:
    """Executes APM scripts with auto‑compilation of .prompt.md files."""

    def __init__(self, compiler=None):
        """
        Initialize script runner with optional compiler.

        Parameters
        ----------
        compiler : Callable[[str, str], str] | None
            A function that takes the path to a .prompt.md file and a
            destination path and writes the compiled content to the
            destination.  If ``None`` a very small default compiler is
            used that simply copies the file content.
        """
        if compiler is None:

            def default_compiler(src: str, dst: str) -> str:
                """Default compiler: copy the file content verbatim."""
                with open(src, "r", encoding="utf-8") as f:
                    content = f.read()
                with open(dst, "w", encoding="utf-8") as f:
                    f.write(content)
                return dst

            self._compiler = default_compiler
        else:
            self._compiler = compiler

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
            ``True`` if the script executed successfully, ``False``
            otherwise.
        """
        config = self._load_config()
        if not config:
            raise FileNotFoundError("apm.yml not found in current directory")

        scripts = config.get("scripts", {})
        if script_name not in scripts:
            raise KeyError(f"Script '{script_name}' not found in apm.yml")

        raw_command = scripts[script_name]
        # Simple parameter substitution using {{param}} syntax
        command = raw_command
        for key, value in params.items():
            command = command.replace(f"{{{{{key}}}}}", value)

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
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as exc:
            print(
                f"Script '{script_name}' failed with exit code {exc.returncode}")
            print(exc.stderr)
            return False
        finally:
            # Clean up compiled prompt files
            for f in compiled_files:
                try:
                    os.remove(f)
                except OSError:
                    pass

    def list_scripts(self) -> Dict[str, str]:
        """
        List all available scripts from apm.yml.

        Returns
        -------
        Dict[str, str]
            Mapping of script names to their commands.
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
        path = Path("apm.yml")
        if not path.is_file():
            return None
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)

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
        compiled_files: List[str] = []

        # Find all .prompt.md references in the command
        # We assume a reference looks like: "prompt: path/to/file.prompt.md"
        prompt_pattern = re.compile(r"prompt:\s*([^\s]+\.prompt\.md)")
        matches = prompt_pattern.findall(command)

        for prompt_path in matches:
            src_path = Path(prompt_path)
            if not src_path.is_file():
                continue

            # Destination path: same directory, .txt extension
            dst_path = src_path.with_suffix(".txt")
            # Compile the prompt
            self._compiler(str(src_path), str(dst_path))
            compiled_files.append(str(dst_path))

            # Replace the original prompt reference with the compiled path
            command = command.replace(
                f"prompt: {prompt_path}", f"prompt: {dst_path}"
            )

        # Transform runtime command placeholders
        # For example, replace "{{prompt_file}}" with the compiled path
        for prompt_path in matches:
            src_path = Path(prompt_path)
            dst_path = src_path.with_suffix(".txt")
            command = self._transform_runtime_command(
                command, str(src_path), "", str(dst_path)
            )

        return command, compiled_files

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
            Compiled prompt content as string (unused here).
        compiled_path : str
            Path to compiled .txt file.

        Returns
        -------
        str
            Transformed command for proper runtime execution.
        """
        # Replace any placeholder that refers to the original prompt file
        # with the compiled path.  The placeholder syntax is assumed to be
        # {{prompt_file}} or similar.
        placeholder = re.escape(prompt_file)
        return re.sub(placeholder, compiled_path, command)
