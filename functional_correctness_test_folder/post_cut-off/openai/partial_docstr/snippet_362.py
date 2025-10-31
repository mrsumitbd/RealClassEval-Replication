
import os
import re
import subprocess
import yaml
from typing import Dict, Optional, Tuple, List


class ScriptRunner:
    """
    A simple script runner that loads script definitions from an `apm.yml` file,
    performs parameter substitution, auto‑compiles `.prompt.md` files, and
    executes the resulting command.
    """

    def __init__(self, compiler=None):
        """
        Parameters
        ----------
        compiler : callable, optional
            A callable that accepts a prompt file path and returns a tuple
            `(compiled_content, compiled_path)`. If not provided, the runner
            will simply copy the prompt file to a temporary location.
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
        if not config or "scripts" not in config:
            return False

        scripts = config["scripts"]
        if script_name not in scripts:
            return False

        command = scripts[script_name]
        # Substitute simple {{param}} placeholders
        for key, value in params.items():
            command = command.replace(f"{{{{{key}}}}}", value)

        compiled_command, compiled_files = self._auto_compile_prompts(
            command, params)

        try:
            result = subprocess.run(
                compiled_command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            # Clean up compiled prompt files
            for f in compiled_files:
                try:
                    os.remove(f)
                except OSError:
                    pass
            return result.returncode == 0
        except subprocess.CalledProcessError:
            return False

    def list_scripts(self) -> Dict[str, str]:
        """
        List all scripts defined in apm.yml.

        Returns
        -------
        Dict[str, str]
            Mapping of script names to their command strings.
        """
        config = self._load_config()
        if not config or "scripts" not in config:
            return {}
        return config["scripts"]

    def _load_config(self) -> Optional[Dict]:
        """
        Load the apm.yml configuration file from the current working directory.

        Returns
        -------
        Optional[Dict]
            Parsed YAML configuration or None if file not found.
        """
        config_path = os.path.join(os.getcwd(), "apm.yml")
        if not os.path.isfile(config_path):
            return None
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _auto_compile_prompts(
        self, command: str, params: Dict[str, str]
    ) -> Tuple[str, List[str]]:
        """
        Auto‑compile .prompt.md files referenced in the command and transform
        runtime commands.

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

        def repl(match: re.Match) -> str:
            prompt_file = match.group(1).strip()
            if not os.path.isabs(prompt_file):
                prompt_file = os.path.join(os.getcwd(), prompt_file)
            if not os.path.isfile(prompt_file):
                return match.group(0)  # leave unchanged

            # Compile the prompt file
            if self.compiler:
                compiled_content, compiled_path = self.compiler(prompt_file)
            else:
                # Default: copy the file to a temp location
                compiled_path = os.path.join(
                    os.getcwd(), f"_compiled_{os.path.basename(prompt_file)}"
                )
                with open(prompt_file, "r", encoding="utf-8") as src, open(
                    compiled_path, "w", encoding="utf-8"
                ) as dst:
                    dst.write(src.read())
                compiled_content = None

            compiled_files.append(compiled_path)
            return compiled_path

        # Replace all {{prompt:...}} placeholders
        compiled_command = re.sub(r"\{\{prompt:(.*?)\}\}", repl, command)
        return compiled_command, compiled_files

    def _transform_runtime_command(
        self, command: str, prompt_file: str, compiled_content: str, compiled_path: str
    ) -> str:
        """
        Transform a runtime command by replacing a prompt placeholder with the
        compiled path.

        Parameters
        ----------
        command : str
            Original command string.
        prompt_file : str
            Path to the original prompt file.
        compiled_content : str
            Compiled content of the prompt file (unused in this simple impl).
        compiled_path : str
            Path to the compiled prompt file.

        Returns
        -------
        str
            Transformed command string.
        """
        placeholder = f"{{{{prompt:{prompt_file}}}}}"
        return command.replace(placeholder, compiled_path)
