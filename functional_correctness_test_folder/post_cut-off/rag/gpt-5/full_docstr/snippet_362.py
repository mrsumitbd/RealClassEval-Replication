from typing import Dict, Optional
import os
import re
import yaml
import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime


class ScriptRunner:
    '''Executes APM scripts with auto-compilation of .prompt.md files.'''

    def __init__(self, compiler=None):
        '''Initialize script runner with optional compiler.'''
        self.compiler = compiler or self._default_compiler
        self._config_cache = None
        self._config_mtime = None
        self.build_dir = Path(".apm_build")
        self.build_dir.mkdir(exist_ok=True)

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

        scripts = config.get("scripts") or {}
        if script_name not in scripts:
            return False

        cmd = scripts[script_name]
        if isinstance(cmd, list):
            command = " && ".join(str(c) for c in cmd)
        elif isinstance(cmd, dict):
            command = str(cmd.get("cmd") or cmd.get("command") or "")
        else:
            command = str(cmd)

        if not command:
            return False

        command = self._substitute_placeholders(command, params)
        compiled_command, _compiled_files = self._auto_compile_prompts(
            command, params)

        env = os.environ.copy()
        for k, v in params.items():
            env_key = f"APM_{str(k).upper()}"
            env[env_key] = str(v)

        result = subprocess.run(compiled_command, shell=True, env=env)
        return result.returncode == 0

    def list_scripts(self) -> Dict[str, str]:
        '''List all available scripts from apm.yml.
        Returns:
            Dict mapping script names to their commands
        '''
        config = self._load_config()
        if not config:
            return {}
        scripts = config.get("scripts") or {}
        out = {}
        for name, cmd in scripts.items():
            if isinstance(cmd, list):
                out[name] = " && ".join(str(c) for c in cmd)
            elif isinstance(cmd, dict):
                out[name] = str(cmd.get("cmd") or cmd.get("command") or "")
            else:
                out[name] = str(cmd)
        return out

    def _load_config(self) -> Optional[Dict]:
        '''Load apm.yml from current directory.'''
        candidates = [Path("apm.yml"), Path("apm.yaml")]
        path = next((p for p in candidates if p.exists()), None)
        if not path:
            return None
        try:
            stat = path.stat()
            mtime = stat.st_mtime
            if self._config_cache is not None and self._config_mtime == mtime:
                return self._config_cache
            with path.open("r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f) or {}
            self._config_cache = cfg
            self._config_mtime = mtime
            return cfg
        except Exception:
            return None

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> tuple[str, list[str]]:
        '''Auto-compile .prompt.md files and transform runtime commands.
        Args:
            command: Original script command
            params: Parameters for compilation
        Returns:
            Tuple of (compiled_command, list_of_compiled_prompt_files)
        '''
        # Find tokens that look like file paths ending with .prompt.md, potentially quoted
        pattern = r'(?P<prefix>@?)(?P<quote>["\']?)(?P<path>[^ "\']+\.prompt\.md)(?P=quote)'
        compiled_files = []
        transformed_command = command

        seen = set()
        for match in re.finditer(pattern, command):
            prompt_file = match.group('path')
            if prompt_file in seen:
                continue
            seen.add(prompt_file)

            src_path = Path(prompt_file)
            if not src_path.exists():
                continue

            try:
                content = src_path.read_text(encoding="utf-8")
            except Exception:
                continue

            compiled_content = self.compiler(content, params)

            compiled_path = self._make_compiled_path(
                src_path, compiled_content, params)
            try:
                Path(compiled_path).parent.mkdir(parents=True, exist_ok=True)
                Path(compiled_path).write_text(
                    compiled_content, encoding="utf-8")
            except Exception:
                continue

            transformed_command = self._transform_runtime_command(
                transformed_command, prompt_file=prompt_file,
                compiled_content=compiled_content, compiled_path=str(
                    compiled_path)
            )
            compiled_files.append(str(compiled_path))

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
        # Replace raw path appearances
        replaced = command.replace(prompt_file, compiled_path)
        # Replace @file (curl-like syntax) appearances
        replaced = replaced.replace(f"@{prompt_file}", f"@{compiled_path}")
        # Replace quoted forms
        for quote in ['"', "'"]:
            replaced = replaced.replace(
                f"{quote}{prompt_file}{quote}", f"{quote}{compiled_path}{quote}")
            replaced = replaced.replace(
                f"{quote}@{prompt_file}{quote}", f"{quote}@{compiled_path}{quote}")
        return replaced

    def _default_compiler(self, markdown: str, params: Dict[str, str]) -> str:
        # Replace {{ var }} placeholders
        def replacer(m):
            key = m.group(1)
            return str(params.get(key, ""))

        compiled = re.sub(r"\{\{\s*([\w\.\-\:]+)\s*\}\}", replacer, markdown)
        # Add a provenance header
        stamp = datetime.utcnow().isoformat() + "Z"
        header = f"<!-- Compiled by ScriptRunner at {stamp} -->\n"
        return header + compiled

    def _substitute_placeholders(self, text: str, params: Dict[str, str]) -> str:
        # Replace {{var}} in command text
        def dbl(m):
            key = m.group(1)
            return str(params.get(key, ""))
        text = re.sub(r"\{\{\s*([\w\.\-\:]+)\s*\}\}", dbl, text)

        # Replace {var} tokens that look safe (avoid formatting braces used by shells)
        # Only replace alphanumeric/underscore names
        def single_format(t: str) -> str:
            # Replace {name} only if present in params
            def repl(m):
                key = m.group(1)
                if key in params:
                    return str(params[key])
                return m.group(0)
            return re.sub(r"\{([A-Za-z_][A-Za-z0-9_\.\-:]*)\}", repl, t)
        text = single_format(text)
        return text

    def _make_compiled_path(self, src_path: Path, compiled_content: str, params: Dict[str, str]) -> Path:
        # Create a deterministic compiled filename within build_dir
        rel = str(src_path)
        slug = re.sub(r"[^\w\.-]+", "_", rel)
        digest_src = hashlib.sha1(rel.encode("utf-8")).hexdigest()[:8]
        digest_content = hashlib.sha1(
            compiled_content.encode("utf-8")).hexdigest()[:8]
        digest_params = hashlib.sha1(json.dumps(
            params, sort_keys=True).encode("utf-8")).hexdigest()[:8]
        filename = f"{slug}.{digest_src}.{digest_params}.{digest_content}.txt"
        return self.build_dir / filename
