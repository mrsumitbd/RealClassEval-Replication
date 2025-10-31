
import os
import subprocess
import yaml
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
            destination path and returns the compiled content.  If
            ``None`` a very small default compiler is used that simply
            copies the file and performs basic placeholder substitution.
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
        """Load apm.yml from the current directory."""
        path = os.path.join(os.getcwd(), "apm.yml")
        if not os.path.isfile(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
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
            Compiled command and list of compiled prompt file paths.
        """
        compiled_files: List[str] = []

        # Find all .prompt.md files in the current directory
        for root, _, files in os.walk(os.getcwd()):
            for fname in files:
                if fname.endswith(".prompt.md"):
                    prompt_path = os.path.join(root, fname)
                    compiled_path = os.path.splitext(prompt_path)[0] + ".txt"

                    # Compile the prompt file
                    compiled_content = self.compiler(
                        prompt_path, compiled_path, params)

                    # Write the compiled content to the .txt file
                    with open(compiled_path, "w", encoding="utf-8") as cf:
                        cf.write(compiled_content)

                    compiled_files.append(compiled_path)

                    # Replace occurrences of the original prompt file in the command
                    command = command.replace(prompt_path, compiled_path)

        return command, compiled_files

    def _transform_runtime_command(
        self, command: str, prompt_file: str, compiled_content: str, compiled_path: str
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
        # In this simplified implementation we just return the command unchanged.
        # The method is kept for compatibility with potential future extensions.
        return command

    # ------------------------------------------------------------------
    # Default compiler
    # ------------------------------------------------------------------
    @staticmethod
    def _default_compiler(
        prompt_path: str, compiled_path: str, params: Dict[str, str]
    ) -> str:
        """
        Default compiler that copies the .prompt.md file and performs
        simple placeholder substitution.

        Parameters
        ----------
        prompt_path : str
            Path to the source .prompt.md file.
        compiled_path : str
            Destination path for the compiled .txt file.
        params : Dict[str, str]
            Parameters for placeholder substitution.

        Returns
        -------
        str
            Compiled content.
        """
        with open(prompt_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Simple placeholder substitution: replace {{key}} with params[key]
        for key, value in params.items():
            content = content.replace(f"{{{{{key}}}}}", value)

        return content
