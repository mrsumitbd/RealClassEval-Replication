from __future__ import annotations

import json
import os
import shlex
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Optional, Tuple, List, Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None  # type: ignore


class ScriptRunner:
    def __init__(self, compiler=None):
        self.compiler = compiler

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        cfg = self._load_config()
        if not cfg:
            return False

        scripts = cfg.get("scripts", cfg) if isinstance(cfg, dict) else {}
        if not isinstance(scripts, dict):
            return False

        script_def = scripts.get(script_name)
        if script_def is None:
            return False

        if isinstance(script_def, dict):
            command = script_def.get("command") or script_def.get("cmd") or ""
        elif isinstance(script_def, str):
            command = script_def
        else:
            return False

        if not command:
            return False

        command = self._format_with_params(command, params)

        try:
            transformed_command, tmp_files = self._auto_compile_prompts(
                command, params)
            try:
                result = subprocess.run(transformed_command, shell=True)
                return result.returncode == 0
            finally:
                for f in tmp_files:
                    try:
                        Path(f).unlink(missing_ok=True)
                    except Exception:
                        pass
        except Exception:
            return False

    def list_scripts(self) -> Dict[str, str]:
        cfg = self._load_config()
        out: Dict[str, str] = {}
        if not cfg:
            return out

        scripts = cfg.get("scripts", cfg) if isinstance(cfg, dict) else {}
        if not isinstance(scripts, dict):
            return out

        for name, val in scripts.items():
            if isinstance(val, dict):
                desc = val.get("description") or val.get(
                    "desc") or val.get("command") or val.get("cmd") or ""
                out[str(name)] = str(desc)
            else:
                out[str(name)] = str(val)
        return out

    def _load_config(self) -> Optional[Dict]:
        cwd = Path.cwd()
        candidates = [
            cwd / "scripts.json",
            cwd / "scripts.yaml",
            cwd / "scripts.yml",
        ]

        for path in candidates:
            if path.is_file():
                try:
                    if path.suffix == ".json":
                        with path.open("r", encoding="utf-8") as f:
                            data = json.load(f)
                            return data if isinstance(data, dict) else None
                    else:
                        if yaml is None:
                            continue
                        with path.open("r", encoding="utf-8") as f:
                            data = yaml.safe_load(f)  # type: ignore
                            return data if isinstance(data, dict) else None
                except Exception:
                    continue
        return None

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> Tuple[str, List[str]]:
        # Identify potential prompt/template file arguments
        # Heuristics:
        # - Flags like --prompt, -p, --template, -t followed by a file
        # - Any argument that is an existing file and has a known textual extension
        known_flags = {"--prompt", "-p", "--template", "-t", "--file", "-f"}
        text_exts = {".prompt", ".tmpl", ".md", ".txt"}

        try:
            args = shlex.split(command)
        except Exception:
            args = command.split()

        compiled_temp_files: List[str] = []
        file_args_indices: List[int] = []

        # Flag-following detection
        i = 0
        while i < len(args):
            arg = args[i]
            if arg in known_flags and i + 1 < len(args):
                candidate = args[i + 1]
                if self._is_text_file(candidate, text_exts):
                    file_args_indices.append(i + 1)
                    i += 2
                    continue
            # Direct file argument
            if self._is_text_file(arg, text_exts):
                file_args_indices.append(i)
            i += 1

        # Deduplicate indices while preserving order
        seen = set()
        file_args_indices = [idx for idx in file_args_indices if not (
            idx in seen or seen.add(idx))]

        # Compile each prompt/template
        for idx in file_args_indices:
            prompt_file = args[idx]
            try:
                content = Path(prompt_file).read_text(encoding="utf-8")
            except Exception:
                # If cannot read, skip this file
                continue

            compiled_content = self._compile_content(content, params)

            # Write compiled content to a temporary file
            suffix = Path(prompt_file).suffix or ".txt"
            tmp = tempfile.NamedTemporaryFile(
                delete=False, suffix=suffix, prefix="compiled_")
            with tmp:
                tmp.write(compiled_content.encode("utf-8"))
            compiled_path = tmp.name
            compiled_temp_files.append(compiled_path)

            # Update the argument to point to compiled file
            args[idx] = compiled_path

            # Also allow transformation on the full command text if needed
            # (basic replacement of original prompt path with compiled path)
            command = self._transform_runtime_command(
                command, prompt_file, compiled_content, compiled_path)

        # Reconstruct command from possibly modified args (prefer args to ensure quoting)
        final_command = shlex.join(args) if hasattr(shlex, "join") else " ".join(
            shlex.quote(a) for a in args)  # type: ignore
        return final_command, compiled_temp_files

    def _transform_runtime_command(self, command: str, prompt_file: str, compiled_content: str, compiled_path: str) -> str:
        # Replace any direct occurrences of original file path with the compiled path
        if prompt_file in command:
            command = command.replace(prompt_file, compiled_path)
        # If placeholder {compiled_content} exists, substitute it
        if "{compiled_content}" in command:
            # For safety, do not inject raw newlines; write to a temp file and replace with path
            tmp = tempfile.NamedTemporaryFile(
                delete=False, suffix=".txt", prefix="compiled_inline_")
            with tmp:
                tmp.write(compiled_content.encode("utf-8"))
            path = tmp.name
            command = command.replace("{compiled_content}", path)
        return command

    @staticmethod
    def _is_text_file(candidate: str, text_exts: set) -> bool:
        try:
            p = Path(candidate)
            return p.is_file() and p.suffix.lower() in text_exts
        except Exception:
            return False

    @staticmethod
    def _format_with_params(text: str, params: Dict[str, Any]) -> str:
        class SafeDict(dict):
            def __missing__(self, key):
                return "{" + key + "}"

        try:
            return text.format_map(SafeDict(params or {}))
        except Exception:
            return text

    def _compile_content(self, content: str, params: Dict[str, str]) -> str:
        if callable(self.compiler):
            try:
                result = self.compiler(content, params)
                if isinstance(result, str):
                    return result
            except Exception:
                pass
        # Fallback: simple formatting
        return self._format_with_params(content, params)
