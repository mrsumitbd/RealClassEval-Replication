from __future__ import annotations

import os
import re
import shlex
import subprocess
from pathlib import Path
from typing import Dict, Optional, List, Tuple

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


class _SafeDict(dict):
    def __missing__(self, key):
        # Leave unknown placeholders intact
        return "{" + key + "}"


def _safe_format(text: str, mapping: Dict[str, str]) -> str:
    return text.format_map(_SafeDict(mapping))


class ScriptRunner:
    '''Executes APM scripts with auto-compilation of .prompt.md files.'''

    def __init__(self, compiler=None):
        '''Initialize script runner with optional compiler.'''
        self.compiler = compiler  # Optional callable(content: str, params: Dict[str,str]) -> str
        self._config_cache: Optional[Dict] = None

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        '''Run a script from apm.yml with parameter substitution.
        Args:
            script_name: Name of the script to run
            params: Parameters for compilation and script execution
        Returns:
            bool: True if script executed successfully
        '''
        cfg = self._load_config()
        if not cfg or "scripts" not in cfg or script_name not in cfg["scripts"]:
            return False

        command_raw = cfg["scripts"][script_name]
        if not isinstance(command_raw, str):
            return False

        # First substitute params into the command string
        command_sub = _safe_format(command_raw, params or {})

        # Auto-compile any .prompt.md files and transform command
        compiled_command, _compiled_files = self._auto_compile_prompts(
            command_sub, params or {})

        # Execute command
        env = os.environ.copy()
        # Expose params as environment variables (uppercased)
        for k, v in (params or {}).items():
            if isinstance(k, str) and isinstance(v, str):
                env[f"APM_{k.upper()}"] = v

        # Prefer running through a shell for pipeline/redirect support
        proc = subprocess.run(compiled_command, shell=True, env=env)
        return proc.returncode == 0

    def list_scripts(self) -> Dict[str, str]:
        '''List all available scripts from apm.yml.
        Returns:
            Dict mapping script names to their commands
        '''
        cfg = self._load_config()
        scripts = cfg.get("scripts", {}) if cfg else {}
        return {k: v for k, v in scripts.items() if isinstance(v, str)}

    def _load_config(self) -> Optional[Dict]:
        '''Load apm.yml from current directory.'''
        if self._config_cache is not None:
            return self._config_cache
        if yaml is None:
            return None

        for fname in ("apm.yml", "apm.yaml"):
            path = Path.cwd() / fname
            if path.exists():
                try:
                    with path.open("r", encoding="utf-8") as f:
                        self._config_cache = yaml.safe_load(f) or {}
                        return self._config_cache
                except Exception:
                    return None
        return None

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> tuple[str, list[str]]:
        '''Auto-compile .prompt.md files and transform runtime commands.
        Args:
            command: Original script command
            params: Parameters for compilation
        Returns:
            Tuple of (compiled_command, list_of_compiled_prompt_files)
        '''
        prompt_paths = self._find_prompt_files_in_command(command)
        compiled_files: List[str] = []
        transformed_command = command

        for prompt_file in prompt_paths:
            compiled_content, compiled_path = self._compile_prompt_file(
                prompt_file, params)
            if compiled_path:
                compiled_files.append(compiled_path)
                transformed_command = self._transform_runtime_command(
                    transformed_command, prompt_file, compiled_content, compiled_path
                )

        return transformed_command, compiled_files

    def _transform_runtime_command(self, command: str, prompt_file: str, compiled_content: str, compiled_path: str) -> str:
        '''Transform runtime commands to their proper execution format.
        Args:
            command: Original command
            prompt_file: Original .prompt.md file path
            compiled_content: Compiled prompt content as string
            compiled_path: Path to compiled .txt file
        Returns:
            Transformed command for proper runtime execution
        '''
        # Replace all appearances of the prompt file path with the compiled path
        # Handle both quoted and unquoted usages.
        def replace_token(cmd: str, original: str, replacement: str) -> str:
            # Replace raw token
            cmd = cmd.replace(original, replacement)
            # Replace quoted forms
            for q in ('"', "'"):
                cmd = cmd.replace(f"{q}{original}{q}", f"{q}{replacement}{q}")
            return cmd

        transformed = replace_token(command, prompt_file, compiled_path)

        # If the command uses @file semantics (some tools read @filename), ensure it refers to compiled file
        for q in ("", "'", '"'):
            transformed = transformed.replace(
                f"@{q}{prompt_file}{q}", f"@{q}{compiled_path}{q}")

        return transformed

    def _find_prompt_files_in_command(self, command: str) -> List[str]:
        # Identify tokens that look like *.prompt.md
        # This captures paths including dashes, underscores, spaces within quotes, etc.
        # 1) Quoted tokens
        quoted = re.findall(r"""(['"])(.+?\.prompt\.md)\1""", command)
        quoted_files = [m[1] for m in quoted]

        # 2) Unquoted tokens (split conservatively)
        tokens = shlex.split(command, posix=True)
        unquoted_files = [t for t in tokens if t.endswith(".prompt.md")]

        # Merge and preserve order as they appear in the original command string
        # We'll scan the command to order the unique matches.
        candidates = list(dict.fromkeys(quoted_files + unquoted_files))

        # Keep only those that literally appear in the command to be safe
        ordered: List[str] = []
        for c in candidates:
            if c in command and c not in ordered:
                ordered.append(c)
        return ordered

    def _compile_prompt_file(self, prompt_path: str, params: Dict[str, str]) -> Tuple[str, str]:
        p = Path(prompt_path)
        if not p.exists():
            return "", ""

        try:
            content = p.read_text(encoding="utf-8")
        except Exception:
            return "", ""

        # Parameter substitution in prompt content
        compiled_content = _safe_format(content, params or {})

        # Optional external compiler hook
        if callable(self.compiler):
            try:
                compiled_content = self.compiler(
                    compiled_content, params or {})
            except Exception:
                # Fallback to unmodified compiled_content on compiler errors
                pass

        # Write to .txt alongside the original
        compiled_path = p.with_suffix("").with_suffix(
            ".txt")  # transforms *.prompt.md -> *.txt
        try:
            compiled_path.write_text(compiled_content, encoding="utf-8")
        except Exception:
            return "", ""

        return compiled_content, str(compiled_path)
