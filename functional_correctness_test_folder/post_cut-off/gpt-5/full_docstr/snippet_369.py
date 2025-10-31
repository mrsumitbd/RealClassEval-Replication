from __future__ import annotations

import os
import re
import shlex
import subprocess
from pathlib import Path
from typing import Dict, Optional, Any, Iterable

try:
    import yaml  # type: ignore
except Exception:
    yaml = None


class _SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"


def _format_with_params(text: str, params: Dict[str, str]) -> str:
    merged: Dict[str, str] = {}
    # params take precedence over env
    merged.update({k: v for k, v in os.environ.items()})
    merged.update({k: str(v) for k, v in params.items()})
    try:
        return text.format_map(_SafeDict(merged))
    except Exception:
        return text


class ScriptRunner:
    '''Executes APM scripts with auto-compilation of .prompt.md files.'''

    def __init__(self, compiler=None):
        '''Initialize script runner with optional compiler.'''
        self.compiler = compiler
        self._build_dir = Path(".apm_build")

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        '''Run a script from apm.yml with parameter substitution.
        Args:
            script_name: Name of the script to run
            params: Parameters for compilation and script execution
        Returns:
            bool: True if script executed successfully
        '''
        config = self._load_config()
        if not config:
            return False

        scripts = config.get("scripts") or config.get("script") or {}
        if not isinstance(scripts, dict):
            return False

        cmd: Any = scripts.get(script_name)
        if cmd is None:
            return False

        if isinstance(cmd, (list, tuple)):
            # Join list command into a single string with proper quoting
            cmd_str = " ".join(shlex.quote(str(part)) for part in cmd)
        else:
            cmd_str = str(cmd)

        # First pass substitution with provided params/env
        cmd_str = _format_with_params(cmd_str, params)

        # Auto-compile prompt files and transform runtime command
        transformed_cmd, _compiled_files = self._auto_compile_prompts(
            cmd_str, params)

        # Execute
        try:
            completed = subprocess.run(
                transformed_cmd,
                shell=True,
                check=False,
            )
            return completed.returncode == 0
        except Exception:
            return False

    def list_scripts(self) -> Dict[str, str]:
        '''List all available scripts from apm.yml.
        Returns:
            Dict mapping script names to their commands
        '''
        config = self._load_config()
        if not config:
            return {}
        scripts = config.get("scripts") or config.get("script") or {}
        if isinstance(scripts, dict):
            return {str(k): str(v) for k, v in scripts.items()}
        return {}

    def _load_config(self) -> Optional[Dict]:
        '''Load apm.yml from current directory.'''
        for name in ("apm.yml", "apm.yaml"):
            apm_path = Path.cwd() / name
            if apm_path.exists() and apm_path.is_file():
                if yaml is None:
                    return None
                try:
                    with apm_path.open("r", encoding="utf-8") as f:
                        data = yaml.safe_load(f) or {}
                        if isinstance(data, dict):
                            return data
                        return {}
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
        pattern = re.compile(
            r'(?P<path>(?:\.{1,2}|[A-Za-z0-9_./\\:-])+\.prompt\.md)\b')
        found: Iterable[re.Match[str]] = list(pattern.finditer(command))
        if not found:
            return command, []

        compiled_files: list[str] = []
        transformed_cmd = command

        unique_paths: Dict[str, str] = {}
        for m in found:
            raw_path = m.group("path")
            # Normalize and keep original token for replacement
            orig_token = raw_path
            # Strip any surrounding quotes for file system operations
            norm_token = raw_path.strip('\'"')
            if norm_token in unique_paths:
                continue
            unique_paths[norm_token] = orig_token

        for prompt_path_str, orig_token in unique_paths.items():
            prompt_path = Path(prompt_path_str)
            # If path is relative, resolve from CWD
            if not prompt_path.is_absolute():
                prompt_path = (Path.cwd() / prompt_path).resolve()

            if not prompt_path.exists() or not prompt_path.is_file():
                # Skip missing prompt files; leave command as-is
                continue

            try:
                with prompt_path.open("r", encoding="utf-8") as f:
                    source = f.read()
            except Exception:
                continue

            # Substitute parameters into the prompt content
            prepared_source = _format_with_params(source, params)

            # Compile using provided compiler if available
            compiled_content = self._compile_prompt(
                prepared_source, str(prompt_path), params)

            # Determine compiled output path inside .apm_build mirroring original structure
            try:
                rel = prompt_path.relative_to(Path.cwd())
            except Exception:
                # If outside CWD, flatten into build dir using safe name
                rel = Path(prompt_path.name)

            compiled_rel = rel.with_suffix(".txt")
            compiled_path = (self._build_dir / compiled_rel).resolve()
            compiled_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                compiled_path.write_text(compiled_content, encoding="utf-8")
            except Exception:
                continue

            compiled_files.append(str(compiled_path))

            # Transform runtime command to point to compiled file/content
            transformed_cmd = self._transform_runtime_command(
                transformed_cmd,
                prompt_file=orig_token,
                compiled_content=compiled_content,
                compiled_path=str(compiled_path),
            )

        return transformed_cmd, compiled_files

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
        # Replace quoted and unquoted occurrences
        candidates = {
            prompt_file,
            prompt_file.strip('"'),
            prompt_file.strip("'"),
        }

        transformed = command
        for token in list(candidates):
            if not token:
                continue
            # Common patterns: @file, < file, --file file, plain token
            patterns = [
                rf'@{re.escape(token)}\b',
                rf'(<\s*){re.escape(token)}\b',
                rf'(\s)--file\s+{re.escape(token)}\b',
                rf'(\s)-f\s+{re.escape(token)}\b',
                rf'(\s)--prompt-file\s+{re.escape(token)}\b',
                rf'(\s)--prompt\s+{re.escape(token)}\b',
                rf'(\s){re.escape(token)}(\s|$)',
                rf'"{re.escape(token)}"',
                rf"'{re.escape(token)}'",
            ]

            for pat in patterns:
                def repl(m: re.Match):
                    s = m.group(0)
                    if s.startswith("@"):
                        return "@" + compiled_path
                    if s.strip().startswith("<"):
                        prefix = m.group(1) if m.lastindex else "< "
                        return f"{prefix}{compiled_path}"
                    if s.strip().startswith("--") or s.strip().startswith("-f"):
                        # Preserve leading space/group then replace token
                        if m.lastindex:
                            lead = m.group(1)
                        else:
                            lead = " "
                        # Rebuild option with compiled path
                        option = s.strip().split()[0]
                        return f"{lead}{option} {compiled_path}"
                    if s.startswith('"') or s.startswith("'"):
                        quote = s[0]
                        return f"{quote}{compiled_path}{quote}"
                    # Plain token replacement
                    # Keep trailing whitespace if any
                    trailing = ""
                    if s.endswith(" "):
                        trailing = " "
                    return compiled_path + trailing

                transformed = re.sub(pat, repl, transformed)

        # Fallback: simple replace if any missed
        for token in candidates:
            if token:
                transformed = transformed.replace(token, compiled_path)

        return transformed

    def _compile_prompt(self, source: str, path: str, params: Dict[str, str]) -> str:
        compiler = self.compiler
        if compiler is None:
            return source
        try:
            # Support objects with .compile(text, params) method
            if hasattr(compiler, "compile") and callable(getattr(compiler, "compile")):
                return compiler.compile(source, params)  # type: ignore
            # Support callable(source, params)
            if callable(compiler):
                # Try (source, params)
                try:
                    return compiler(source, params)  # type: ignore
                except TypeError:
                    # Try (path, source, params)
                    return compiler(path, source, params)  # type: ignore
        except Exception:
            return source
        return source
