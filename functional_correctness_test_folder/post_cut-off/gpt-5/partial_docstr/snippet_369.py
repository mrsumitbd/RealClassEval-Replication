from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import tempfile
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple


class ScriptRunner:
    '''Executes APM scripts with auto-compilation of .prompt.md files.'''

    def __init__(self, compiler: Optional[Callable[[str, Dict[str, str]], Tuple[str, str]]] = None):
        self.compiler = compiler

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        cfg = self._load_config()
        if not cfg:
            return False
        scripts = cfg.get("scripts", {})
        command = scripts.get(script_name)
        if not command:
            return False

        command = self._apply_params_to_text(command, params)

        try:
            transformed_command, compiled_files = self._auto_compile_prompts(
                command, params)
        except Exception:
            return False

        try:
            proc = subprocess.run(transformed_command, shell=True)
            success = proc.returncode == 0
        finally:
            for p in compiled_files:
                try:
                    Path(p).unlink(missing_ok=True)
                except Exception:
                    pass

        return success

    def list_scripts(self) -> Dict[str, str]:
        cfg = self._load_config()
        if not cfg:
            return {}
        scripts = cfg.get("scripts", {})
        if not isinstance(scripts, dict):
            return {}
        return {str(k): str(v) for k, v in scripts.items()}

    def _load_config(self) -> Optional[Dict]:
        # Try apm.json in current working directory
        candidates = [Path.cwd() / "apm.json", Path.cwd() / ".apm.json"]
        for p in candidates:
            if p.is_file():
                try:
                    with p.open("r", encoding="utf-8") as f:
                        return json.load(f)
                except Exception:
                    return None
        return None

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> tuple[str, list[str]]:
        args = self._safe_split_command(command)
        prompt_files: List[str] = []
        for a in args:
            # Detect literal paths that end with .prompt.md and exist, or paths that end with .prompt.md regardless of existence
            if isinstance(a, str) and a.endswith(".prompt.md"):
                prompt_files.append(a)

        compiled_paths: List[str] = []
        transformed_command = command

        for prompt_path in prompt_files:
            compiled_content, compiled_path = self._compile_prompt(
                prompt_path, params)
            transformed_command = self._transform_runtime_command(
                transformed_command, prompt_path, compiled_content, compiled_path
            )
            compiled_paths.append(compiled_path)

        # Also apply parameter substitution on the transformed command in case new parts appeared
        transformed_command = self._apply_params_to_text(
            transformed_command, params)
        return transformed_command, compiled_paths

    def _transform_runtime_command(self, command: str, prompt_file: str, compiled_content: str, compiled_path: str) -> str:
        # Replace any occurrence of the original prompt file path with the compiled path, including quoted variants
        replacements = {prompt_file: compiled_path}

        # Handle quoted forms
        for q in ['"', "'"]:
            replacements[f"{q}{prompt_file}{q}"] = f"{q}{compiled_path}{q}"

        # Apply replacements
        for src, dst in sorted(replacements.items(), key=lambda x: -len(x[0])):
            command = command.replace(src, dst)

        # Support inline expansion marker: @inline(prompt.md) -> compiled content written to a temp file (already done)
        # We consider any @inline(<prompt_file>) occurrences as well
        inline_pattern = re.compile(
            r"@inline\(\s*" + re.escape(prompt_file) + r"\s*\)")
        if inline_pattern.search(command):
            # Replace inline with compiled path; if consumers want inline content, they can cat the file
            command = inline_pattern.sub(compiled_path, command)

        return command

    def _compile_prompt(self, prompt_path: str, params: Dict[str, str]) -> Tuple[str, str]:
        if self.compiler is not None:
            compiled_content, compiled_path = self.compiler(
                prompt_path, params)
            self._ensure_file_with_content(compiled_path, compiled_content)
            return compiled_content, compiled_path

        # Default compiler: read .prompt.md, apply simple templating, write to a temp file
        source = self._read_text_file(prompt_path)
        compiled_content = self._apply_params_to_text(source, params)

        # Write to a deterministically named temp file in the system temp dir
        base = Path(prompt_path).name
        out_name = base.replace(".prompt.md", ".compiled.md")
        compiled_path = str(Path(tempfile.gettempdir()) / out_name)

        self._ensure_file_with_content(compiled_path, compiled_content)
        return compiled_content, compiled_path

    def _apply_params_to_text(self, text: str, params: Dict[str, str]) -> str:
        if not params:
            return text

        # Replace {{key}}, ${key}, and {key}
        def replace_all(s: str, key: str, val: str) -> str:
            patterns = [
                "{{" + key + "}}",
                "${" + key + "}",
                "{" + key + "}",
                f"<<{key}>>",
            ]
            for pat in patterns:
                s = s.replace(pat, val)
            return s

        for k, v in params.items():
            text = replace_all(text, str(k), str(v))
        return text

    def _safe_split_command(self, command: str) -> List[str]:
        try:
            return shlex.split(command, posix=os.name != "nt")
        except Exception:
            return command.split()

    def _read_text_file(self, path: str) -> str:
        p = Path(path)
        if not p.is_file():
            return ""
        with p.open("r", encoding="utf-8") as f:
            return f.read()

    def _ensure_file_with_content(self, path: str, content: str) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", encoding="utf-8") as f:
            f.write(content)
