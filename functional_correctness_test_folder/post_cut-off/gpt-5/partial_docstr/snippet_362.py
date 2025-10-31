from __future__ import annotations

import os
import re
import shlex
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Optional, List, Tuple

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


class ScriptRunner:
    def __init__(self, compiler=None):
        self.compiler = compiler
        self._config = None

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        cfg = self._load_config()
        if not cfg or "scripts" not in cfg:
            return False

        scripts = cfg.get("scripts", {})
        command = scripts.get(script_name)
        if command is None:
            return False

        if isinstance(command, list):
            command = " && ".join(map(str, command))
        else:
            command = str(command)

        try:
            formatted_command = command.format_map(DefaultDict(params))
        except Exception:
            formatted_command = command

        compiled_command, _compiled_files = self._auto_compile_prompts(
            formatted_command, params)

        env = os.environ.copy()
        # Expose params to the environment as APM_PARAM_<KEY>=value
        for k, v in params.items():
            if isinstance(k, str) and isinstance(v, str):
                env_key = f"APM_PARAM_{re.sub(r'[^A-Za-z0-9_]', '_', k).upper()}"
                env[env_key] = v

        result = subprocess.run(compiled_command, shell=True, env=env)
        return result.returncode == 0

    def list_scripts(self) -> Dict[str, str]:
        cfg = self._load_config()
        if not cfg or "scripts" not in cfg or not isinstance(cfg["scripts"], dict):
            return {}
        scripts = cfg["scripts"]
        out: Dict[str, str] = {}
        for k, v in scripts.items():
            if isinstance(v, list):
                out[str(k)] = " && ".join(map(str, v))
            else:
                out[str(k)] = str(v)
        return out

    def _load_config(self) -> Optional[Dict]:
        if self._config is not None:
            return self._config
        cfg_path = None
        for name in ("apm.yml", "apm.yaml"):
            p = Path.cwd() / name
            if p.is_file():
                cfg_path = p
                break
        if cfg_path is None:
            self._config = None
            return None
        if yaml is None:
            self._config = None
            return None
        try:
            with cfg_path.open("r", encoding="utf-8") as f:
                self._config = yaml.safe_load(f) or {}
        except Exception:
            self._config = None
        return self._config

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> tuple[str, list[str]]:
        tokens = self._shell_split(command)
        prompt_files = self._find_prompt_files(tokens)
        if not prompt_files:
            return command, []

        compiled_files: List[str] = []
        # Temporary directory lifecycle tied to this compilation
        with tempfile.TemporaryDirectory(prefix="apm_prompts_") as tmpdir:
            transformed = command
            for pf in prompt_files:
                src_path = Path(pf)
                try:
                    content = src_path.read_text(encoding="utf-8")
                except Exception:
                    # If file can't be read, leave as-is
                    continue

                compiled_content = self._compile_content(content, params)
                compiled_path = str(
                    Path(tmpdir) / (src_path.stem + ".compiled.txt"))
                try:
                    Path(compiled_path).write_text(
                        compiled_content, encoding="utf-8")
                except Exception:
                    continue

                compiled_files.append(compiled_path)
                transformed = self._transform_runtime_command(
                    transformed, pf, compiled_content, compiled_path)

            # Execute transformed command while temp dir exists, then return transformed command string that
            # still points to files in temp dir; however, since we return after tempdir deletion, we should
            # instead inline a here-string fallback if any compiled files are used. To avoid complexity,
            # we will re-write transformed command to use process substitution when available, else keep paths
            # (which may be removed). To ensure correctness, we will persist compiled files outside temp dir.
            # Re-emit compiled files into a persistent temp dir.
            if compiled_files:
                stable_dir = tempfile.mkdtemp(prefix="apm_prompts_")
                stable_transformed = transformed
                for pf in prompt_files:
                    src_path = Path(pf)
                    tmp_compiled = Path(tmpdir) / \
                        (src_path.stem + ".compiled.txt")
                    stable_compiled = Path(stable_dir) / \
                        (src_path.stem + ".compiled.txt")
                    if tmp_compiled.exists():
                        try:
                            stable_compiled.write_text(tmp_compiled.read_text(
                                encoding="utf-8"), encoding="utf-8")
                        except Exception:
                            continue
                        # Replace paths to tmpdir with stable paths
                        stable_transformed = stable_transformed.replace(
                            str(tmp_compiled), str(stable_compiled))
                transformed = stable_transformed
                # Update compiled_files list to stable paths
                compiled_files = []
                for pf in prompt_files:
                    src_path = Path(pf)
                    stable_compiled = Path(stable_dir) / \
                        (src_path.stem + ".compiled.txt")
                    if stable_compiled.exists():
                        compiled_files.append(str(stable_compiled))

            return transformed, compiled_files

    def _transform_runtime_command(self, command: str, prompt_file: str, compiled_content: str, compiled_path: str) -> str:
        # Replace exact token occurrences of the prompt file with the compiled file path.
        # Also replace quoted occurrences.
        patterns = [
            re.escape(prompt_file),
            re.escape(str(Path(prompt_file).resolve())),
            re.escape(str(Path(prompt_file))),
        ]
        out = command
        for pat in patterns:
            out = re.sub(rf'(?<!\S){pat}(?!\S)', compiled_path, out)
            out = out.replace(f'"{pat}"', f'"{compiled_path}"')
            out = out.replace(f"'{pat}'", f"'{compiled_path}'")
        return out

    def _compile_content(self, content: str, params: Dict[str, str]) -> str:
        if self.compiler and hasattr(self.compiler, "compile"):
            try:
                return self.compiler.compile(content, params)
            except Exception:
                pass
        try:
            return content.format_map(DefaultDict(params))
        except Exception:
            return content

    def _shell_split(self, command: str) -> List[str]:
        try:
            return shlex.split(command)
        except Exception:
            # Fallback: naive split
            return command.split()

    def _find_prompt_files(self, tokens: List[str]) -> List[str]:
        prompt_files: List[str] = []
        for t in tokens:
            # strip quotes if present
            if (t.startswith("'") and t.endswith("'")) or (t.startswith('"') and t.endswith('"')):
                t_unq = t[1:-1]
            else:
                t_unq = t
            if t_unq.endswith(".prompt.md"):
                p = Path(t_unq)
                if p.exists() and p.is_file():
                    prompt_files.append(t_unq)
        return prompt_files


class DefaultDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"
