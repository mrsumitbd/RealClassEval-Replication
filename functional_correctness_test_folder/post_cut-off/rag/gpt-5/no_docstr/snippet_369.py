from typing import Dict, Optional, List, Tuple
import os
import re
import json
import subprocess
from pathlib import Path

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None


class _DefaultPromptCompiler:
    def __init__(self, build_dir: Optional[Path] = None):
        self.build_dir = Path(build_dir) if build_dir else Path(".apm_build")
        self.build_dir.mkdir(parents=True, exist_ok=True)

    def _substitute(self, text: str, params: Dict[str, str]) -> str:
        def repl(m):
            key = m.group(1).strip()
            return str(params.get(key, m.group(0)))
        return re.sub(r"\{\{\s*([A-Za-z0-9_\-\.]+)\s*\}\}", repl, text)

    def compile(self, source_path: str, params: Dict[str, str]) -> Tuple[str, str]:
        src = Path(source_path)
        if not src.exists():
            raise FileNotFoundError(f"Prompt file not found: {source_path}")
        with src.open("r", encoding="utf-8") as f:
            content = f.read()
        compiled = self._substitute(content, params)
        out_name = src.with_suffix("").name + ".txt"
        out_path = self.build_dir / out_name
        with out_path.open("w", encoding="utf-8") as f:
            f.write(compiled)
        return compiled, str(out_path)


class ScriptRunner:
    '''Executes APM scripts with auto-compilation of .prompt.md files.'''

    def __init__(self, compiler=None):
        '''Initialize script runner with optional compiler.'''
        self.compiler = compiler if compiler is not None else _DefaultPromptCompiler()

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        '''Run a script from apm.yml with parameter substitution.
        Args:
            script_name: Name of the script to run
            params: Parameters for compilation and script execution
        Returns:
            bool: True if script executed successfully
        '''
        cfg = self._load_config()
        if not cfg:
            return False
        scripts = cfg.get("scripts", {})
        if script_name not in scripts:
            return False
        raw = scripts[script_name]
        if isinstance(raw, dict):
            command = raw.get("cmd") or raw.get("command") or ""
        else:
            command = str(raw)

        command = self._substitute_params_in_text(command, params)
        command, _ = self._auto_compile_prompts(command, params)

        env = os.environ.copy()
        env.update({k: str(v) for k, v in params.items()})
        env.setdefault("APM_PARAMS_JSON", json.dumps(params))

        try:
            proc = subprocess.run(command, shell=True, env=env)
            return proc.returncode == 0
        except Exception:
            return False

    def list_scripts(self) -> Dict[str, str]:
        '''List all available scripts from apm.yml.
        Returns:
            Dict mapping script names to their commands
        '''
        cfg = self._load_config()
        if not cfg:
            return {}
        scripts = cfg.get("scripts", {})
        result: Dict[str, str] = {}
        for name, val in scripts.items():
            if isinstance(val, dict):
                cmd = val.get("cmd") or val.get("command")
                if cmd is None:
                    continue
                result[name] = str(cmd)
            else:
                result[name] = str(val)
        return result

    def _load_config(self) -> Optional[Dict]:
        '''Load apm.yml from current directory.'''
        if yaml is None:
            return None
        for fname in ("apm.yml", "apm.yaml"):
            p = Path(fname)
            if p.exists():
                try:
                    with p.open("r", encoding="utf-8") as f:
                        data = yaml.safe_load(f) or {}
                    if isinstance(data, dict):
                        return data
                    return None
                except Exception:
                    return None
        return None

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> Tuple[str, List[str]]:
        '''Auto-compile .prompt.md files and transform runtime commands.
        Args:
            command: Original script command
            params: Parameters for compilation
        Returns:
            Tuple of (compiled_command, list_of_compiled_prompt_files)
        '''
        pattern = r'''(?P<prefix>@|<|--?[A-Za-z0-9_\-\.]+=|(?<!\S))(?P<q>["']?)(?P<path>[^"'\s]+\.prompt\.md)(?P=q)'''
        compiled_files: List[str] = []
        seen: set = set()

        def repl(m):
            prefix = m.group("prefix")
            path = m.group("path")
            if path in seen:
                compiled_path = compiled_files[[
                    cf.split(" -> ")[0] for cf in compiled_files].index(path)].split(" -> ")[1]
            else:
                compiled_content, compiled_path = self.compiler.compile(
                    path, params)
                compiled_files.append(f"{path} -> {compiled_path}")
                seen.add(path)
            transformed = self._transform_runtime_command(
                command="", prompt_file=path, compiled_content="", compiled_path=compiled_path)
            # transformed here returns just a path replacement logic; we only need the compiled path piece
            # Keep the same quoting behavior as input
            q = m.group("q") or ""
            return f"{prefix}{q}{compiled_path}{q}"

        new_command = re.sub(pattern, repl, command)
        return new_command, compiled_files

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
        if not command:
            return compiled_path
        escaped = re.escape(prompt_file)

        replacements = [
            (rf"@{escaped}", f"@{compiled_path}"),
            (rf"<\s*{escaped}", f"< {compiled_path}"),
            (rf'="{escaped}"', f'="{compiled_path}"'),
            (rf"='{escaped}'", f"='{compiled_path}'"),
            (rf"={escaped}", f"={compiled_path}"),
            (rf'"{escaped}"', f'"{compiled_path}"'),
            (rf"'{escaped}'", f"'{compiled_path}'"),
            (rf"{escaped}", f"{compiled_path}"),
        ]

        new_cmd = command
        for pat, rep in replacements:
            new_cmd = re.sub(pat, rep, new_cmd)
        return new_cmd

    def _substitute_params_in_text(self, text: str, params: Dict[str, str]) -> str:
        def repl(m):
            key = m.group(1).strip()
            return str(params.get(key, m.group(0)))
        return re.sub(r"\{\{\s*([A-Za-z0-9_\-\.]+)\s*\}\}", repl, text)
