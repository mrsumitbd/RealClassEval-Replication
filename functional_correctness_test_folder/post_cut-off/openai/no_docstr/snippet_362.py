
import os
import json
import subprocess
import tempfile
import shutil
from typing import Dict, Optional, Tuple, List


class ScriptRunner:
    """
    A simple script runner that can load scripts from a directory,
    automatically compile prompt files referenced in the script,
    and execute the resulting command.
    """

    def __init__(self, compiler=None):
        """
        :param compiler: A callable that takes a prompt string and returns a compiled string.
        """
        self.compiler = compiler
        self.script_dir = os.getenv("SCRIPT_DIR", os.getcwd())
        self.config = self._load_config()

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        """
        Execute a script with the given parameters.

        :param script_name: Name of the script file (without path).
        :param params: Dictionary of parameters to substitute into the script.
        :return: True if the script executed successfully, False otherwise.
        """
        scripts = self.list_scripts()
        if script_name not in scripts:
            raise FileNotFoundError(
                f"Script '{script_name}' not found in {self.script_dir}")

        script_path = scripts[script_name]
        with open(script_path, "r", encoding="utf-8") as f:
            command = f.read()

        # Substitute parameters
        for key, value in params.items():
            command = command.replace(f"${{{key}}}", value)

        # Auto‑compile prompts referenced in the command
        command, compiled_files = self._auto_compile_prompts(command, params)

        # Transform the command for runtime execution
        if compiled_files:
            # For simplicity, use the first compiled file
            prompt_file, compiled_content, compiled_path = compiled_files[0]
            command = self._transform_runtime_command(
                command, prompt_file, compiled_content, compiled_path
            )

        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.script_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as exc:
            print(f"Script failed: {exc.stderr}")
            return False
        finally:
            # Clean up temporary compiled files
            for _, _, compiled_path in compiled_files:
                try:
                    os.remove(compiled_path)
                except OSError:
                    pass

    def list_scripts(self) -> Dict[str, str]:
        """
        List all script files in the script directory.

        :return: Dictionary mapping script names to absolute paths.
        """
        scripts = {}
        for entry in os.listdir(self.script_dir):
            full_path = os.path.join(self.script_dir, entry)
            if os.path.isfile(full_path) and entry.endswith((".sh", ".py", ".bat", ".cmd")):
                scripts[entry] = full_path
        return scripts

    def _load_config(self) -> Optional[Dict]:
        """
        Load a JSON configuration file named 'config.json' from the script directory.

        :return: Configuration dictionary or None if not found.
        """
        config_path = os.path.join(self.script_dir, "config.json")
        if not os.path.isfile(config_path):
            return None
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def _auto_compile_prompts(
        self, command: str, params: Dict[str, str]
    ) -> Tuple[str, List[Tuple[str, str, str]]]:
        """
        Detect prompt files referenced in the command and compile them.

        :param command: The command string to process.
        :param params: Parameters that may contain prompt file paths.
        :return: Tuple of (updated command, list of tuples (prompt_file, compiled_content, compiled_path)).
        """
        compiled_files: List[Tuple[str, str, str]] = []

        # Find all placeholders like ${prompt_file}
        for key, value in params.items():
            if value.endswith(".prompt"):
                prompt_path = os.path.join(self.script_dir, value)
                if not os.path.isfile(prompt_path):
                    continue
                with open(prompt_path, "r", encoding="utf-8") as pf:
                    prompt_content = pf.read()
                compiled_content = (
                    self.compiler(
                        prompt_content) if self.compiler else prompt_content
                )
                # Write compiled content to a temporary file
                tmp_fd, tmp_path = tempfile.mkstemp(
                    suffix=".txt", dir=self.script_dir)
                os.close(tmp_fd)
                with open(tmp_path, "w", encoding="utf-8") as tf:
                    tf.write(compiled_content)
                # Replace placeholder in command
                command = command.replace(f"${{{key}}}", tmp_path)
                compiled_files.append((value, compiled_content, tmp_path))

        return command, compiled_files

    def _transform_runtime_command(
        self, command: str, prompt_file: str, compiled_content: str, compiled_path: str
    ) -> str:
        """
        Perform any final transformations on the command before execution.

        :param command: The command string after prompt compilation.
        :param prompt_file: Original prompt file name.
        :param compiled_content: The compiled prompt content.
        :param compiled_path: Path to the compiled prompt file.
        :return: The transformed command string.
        """
        # Example: replace placeholders for compiled content and path
        command = command.replace("{compiled_content}", compiled_content)
        command = command.replace("{compiled_path}", compiled_path)
        command = command.replace("{prompt_file}", prompt_file)
        return command
