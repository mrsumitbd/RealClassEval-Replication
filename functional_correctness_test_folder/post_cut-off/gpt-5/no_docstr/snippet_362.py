from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Optional, List, Tuple


class ScriptRunner:
    def __init__(self, compiler=None):
        self.compiler = compiler
        self._config = self._load_config()
        self._project_root = Path.cwd()
        self._compiled_dir = self._project_root / ".compiled_prompts"
        self._compiled_dir.mkdir(exist_ok=True)

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        cfg = self._config or {}
        scripts = cfg.get("scripts", cfg if isinstance(cfg, dict) else {})
        if not isinstance(scripts, dict):
            return False

        entry = scripts.get(script_name)
        if entry is None:
            return False

        if isinstance(entry, str):
            command = entry
        elif isinstance(entry, dict):
            command = entry.get("command") or ""
        else:
            return False

        if not command:
            return False

        command = self._apply_param_substitutions(command, params)
        command, _ = self._auto_compile_prompts(command, params)

        try:
            proc = subprocess.run(
                command,
                shell=True,
                check=False,
                cwd=self._project_root,
                env={**os.environ, **{str(k): str(v)
                                      for k, v in (params or {}).items()}},
            )
            return proc.returncode == 0
        except Exception:
            return False

    def list_scripts(self) -> Dict[str, str]:
        cfg = self._config or {}
        scripts = cfg.get("scripts", cfg if isinstance(cfg, dict) else {})
        out: Dict[str, str] = {}
        if not isinstance(scripts, dict):
            return out
        for name, entry in scripts.items():
            if isinstance(entry, str):
                out[name] = entry
            elif isinstance(entry, dict):
                desc = entry.get("description") or entry.get("command") or ""
                out[name] = str(desc)
        return out

    def _load_config(self) -> Optional[Dict]:
        candidates = [
            "scripts.yaml",
            "scripts.yml",
            "scripts.json",
            ".scripts.yaml",
            ".scripts.yml",
            ".scripts.json",
        ]
        for fname in candidates:
            p = Path(fname)
            if not p.exists():
                continue
            try:
                if p.suffix in {".yaml", ".yml"}:
                    try:
                        import yaml  # type: ignore
                    except Exception:
                        continue
                    with p.open("r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                        if isinstance(data, dict):
                            return data
                elif p.suffix == ".json":
                    with p.open("r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, dict):
                            return data
            except Exception:
                continue
        return None

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> tuple[str, list[str]]:
        if not command:
            return command, []

        compiled_paths: List[str] = []

        # Find tokens like {{prompt:path/to/file.ext}}
        prompt_pattern = re.compile(r"\{\{\s*prompt\s*:\s*([^}]+?)\s*\}\}")
        matches = list(prompt_pattern.finditer(command))
        if not matches:
            return command, compiled_paths

        new_command = command
        for m in matches:
            raw_path = m.group(1).strip()
            prompt_file = str((self._project_root / raw_path).resolve())

            compiled_content, compiled_path = self._compile_single_prompt(
                prompt_file, params)
            compiled_paths.append(compiled_path)

            new_command = self._transform_runtime_command(
                new_command, raw_path, compiled_content, compiled_path)

        return new_command, compiled_paths

    def _transform_runtime_command(self, command: str, prompt_file: str, compiled_content: str, compiled_path: str) -> str:
        # Replace all variants of the token referencing this prompt file.
        # Variants considered: {{prompt:path}}, {{ prompt : path }}, with any spaces around colon.
        # Use regex to find tokens with this specific file path (normalized trimmed string match).
        file_escaped = re.escape(prompt_file)
        pattern = re.compile(
            r"\{\{\s*prompt\s*:\s*" + file_escaped + r"\s*\}\}")
        command = pattern.sub(compiled_path, command)

        # Also try replacing with absolute path forms if the command included them
        abs_escaped = re.escape(str(Path(prompt_file).resolve()))
        pattern_abs = re.compile(
            r"\{\{\s*prompt\s*:\s*" + abs_escaped + r"\s*\}\}")
        command = pattern_abs.sub(compiled_path, command)

        return command

    # Helpers

    def _apply_param_substitutions(self, command: str, params: Dict[str, str]) -> str:
        if not params:
            return command

        # Replace {{param}} placeholders (but not {{prompt:...}})
        def replace_var(m: re.Match) -> str:
            inner = m.group(1).strip()
            if inner.startswith("prompt:"):
                return m.group(0)
            return str(params.get(inner, ""))

        command = re.sub(r"\{\{\s*([^}:]+)\s*\}\}", replace_var, command)

        # Also support simple str.format style {param}, but avoid replacing braces used by shell or JSON by requiring alnum_ only
        def brace_replace(m: re.Match) -> str:
            key = m.group(1)
            return str(params.get(key, m.group(0)))

        command = re.sub(r"\{([A-Za-z_][A-Za-z0-9_]*)\}",
                         brace_replace, command)

        return command

    def _compile_single_prompt(self, prompt_path: str, params: Dict[str, str]) -> Tuple[str, str]:
        # If a compiler is provided and has a compatible interface, defer to it.
        compiled_content: Optional[str] = None
        compiled_path: Optional[str] = None

        if self.compiler is not None:
            # Try common method names
            try:
                if hasattr(self.compiler, "compile_prompt"):
                    compiled_content, compiled_path = self.compiler.compile_prompt(
                        prompt_path, params)  # type: ignore
                elif hasattr(self.compiler, "compile"):
                    result = self.compiler.compile(
                        prompt_path, params)  # type: ignore
                    if isinstance(result, tuple) and len(result) == 2:
                        compiled_content, compiled_path = result  # type: ignore
            except Exception:
                # Fall back to internal compilation
                compiled_content, compiled_path = None, None

        if compiled_content is None or compiled_path is None:
            compiled_content = self._default_compile_prompt(
                prompt_path, params)
            compiled_path = self._write_compiled_prompt(
                prompt_path, compiled_content)

        return compiled_content, compiled_path

    def _default_compile_prompt(self, prompt_path: str, params: Dict[str, str]) -> str:
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            content = ""

        # Simple templating: replace {{key}} and {key} using params
        def replace_var(m: re.Match) -> str:
            key = m.group(1).strip()
            return str(params.get(key, ""))

        content = re.sub(
            r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}", replace_var, content)
        content = re.sub(r"\{([A-Za-z_][A-Za-z0-9_]*)\}", replace_var, content)
        return content

    def _write_compiled_prompt(self, prompt_path: str, compiled_content: str) -> str:
        # Deterministic filename based on content and source path
        h = hashlib.sha256()
        h.update(prompt_path.encode("utf-8", errors="ignore"))
        h.update(b"\x00")
        h.update(compiled_content.encode("utf-8", errors="ignore"))
        name = f"{Path(prompt_path).stem}-{h.hexdigest()[:16]}.txt"

        # Ensure directory exists and write atomically
        target = self._compiled_dir / name
        tmp_fd, tmp_path = tempfile.mkstemp(
            prefix=".tmp_", dir=str(self._compiled_dir))
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                f.write(compiled_content)
            shutil.move(tmp_path, target)
        finally:
            try:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except Exception:
                pass
        return str(target)
