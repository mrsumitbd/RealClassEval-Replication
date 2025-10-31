
import os
import re
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Optional, Tuple, List


class ScriptRunner:
    '''Executes APM scripts with auto-compilation of .prompt.md files.'''

    def __init__(self, compiler=None):
        """
        :param compiler: Optional object with a `compile(file_path: str) -> str` method.
        """
        self.compiler = compiler
        self.config = self._load_config()
        self.scripts_dir = Path(self.config.get(
            "scripts_dir", "scripts")) if self.config else Path("scripts")

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        """
        Execute the script identified by `script_name` with the given parameters.
        Parameters are passed as environment variables.
        """
        script_path = self._find_script_path(script_name)
        if not script_path:
            raise FileNotFoundError(
                f"Script '{script_name}' not found in {self.scripts_dir}")

        # Read script content
        with open(script_path, "r", encoding="utf-8") as f:
            command = f.read()

        # Auto-compile any .prompt.md references
        command, compiled_files = self._auto_compile_prompts(command, params)

        # Transform command if needed
        command = self._transform_runtime_command(command, compiled_files)

        # Prepare environment
        env = os.environ.copy()
        env.update(params)

        # Execute the command
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                env=env,
                text=True,
            )
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(
                f"Script '{script_name}' failed with exit code {e.returncode}")
            print(e.stderr)
            return False
        finally:
            # Clean up compiled temp files
            for tmp_path in compiled_files:
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass

    def list_scripts(self) -> Dict[str, str]:
        """
        Return a mapping of script names (without extension) to their full paths.
        """
        scripts = {}
        if not self.scripts_dir.exists():
            return scripts
        for ext in ("*.sh", "*.py", "*.bat", "*.cmd"):
            for path in self.scripts_dir.rglob(ext):
                name = path.stem
                scripts[name] = str(path.resolve())
        return scripts

    def _load_config(self) -> Optional[Dict]:
        """
        Load configuration from 'apm_config.json' if it exists.
        """
        config_path = Path("apm_config.json")
        if config_path.is_file():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return None
        return None

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> Tuple[str, List[str]]:
        """
        Find all .prompt.md references in the command, compile them, and replace
        the original paths with temporary compiled file paths.
        Returns the updated command and a list of temporary file paths created.
        """
        prompt_pattern = re.compile(r"([^\s'\"`]+\.prompt\.md)")
        matches = prompt_pattern.findall(command)
        temp_files = []

        for prompt_path in matches:
            abs_prompt = Path(prompt_path).expanduser().resolve()
            if not abs_prompt.is_file():
                continue

            # Compile content
            if self.compiler and hasattr(self.compiler, "compile"):
                compiled_content = self.compiler.compile(str(abs_prompt))
            else:
                compiled_content = abs_prompt.read_text(encoding="utf-8")

            # Write to temp file
            tmp_fd, tmp_path = tempfile.mkstemp(
                suffix=".txt", prefix="compiled_", text=True)
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as tmp_file:
                tmp_file.write(compiled_content)
            temp_files.append(tmp_path)

            # Replace original path with temp path
            command = command.replace(str(abs_prompt), tmp_path)

        return command, temp_files

    def _transform_runtime_command(self, command: str, prompt_file: str, compiled_content: str, compiled_path: str) -> str:
        """
        Hook for further transformation of the runtime command.
        Default implementation returns the command unchanged.
        """
        return command

    # Helper method to locate script file
    def _find_script_path(self, script_name: str) -> Optional[Path]:
        """
        Resolve a script name to its full path within the scripts directory.
        """
        for ext in ("sh", "py", "bat", "cmd"):
            candidate = self.scripts_dir / f"{script_name}.{ext}"
            if candidate.is_file():
                return candidate
        # If script_name already contains an extension
        candidate = self.scripts_dir / script_name
        if candidate.is_file():
            return candidate
        return None
