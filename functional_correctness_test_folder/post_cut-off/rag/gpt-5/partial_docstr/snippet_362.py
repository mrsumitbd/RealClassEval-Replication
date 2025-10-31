import os
import re
import shlex
import subprocess
import logging
from pathlib import Path
from typing import Dict, Optional, Callable, List

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None  # type: ignore

logger = logging.getLogger(__name__)


class ScriptRunner:
    '''Executes APM scripts with auto-compilation of .prompt.md files.'''

    def __init__(self, compiler: Optional[Callable[[str, Dict[str, str]], str]] = None):
        '''Initialize script runner with optional compiler.'''
        self.compiler = compiler or self._default_compiler

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
            logger.error("apm.yml not found or could not be parsed.")
            return False

        scripts = {}
        if isinstance(config, dict):
            scripts = config.get('scripts', {})
            # Some users may define scripts at top-level. Merge conservatively.
            if not isinstance(scripts, dict):
                scripts = {}
            for k, v in config.items():
                if k != 'scripts' and isinstance(v, (str, list, dict)):
                    scripts.setdefault(k, v)

        if script_name not in scripts:
            logger.error("Script '%s' not found in apm.yml", script_name)
            return False

        entry = scripts[script_name]
        cmd = ""
        cwd = None
        merge_env: Dict[str, str] = {}

        if isinstance(entry, str):
            cmd = entry
        elif isinstance(entry, list):
            cmd = " && ".join([str(x) for x in entry])
        elif isinstance(entry, dict):
            # Support minimal structure:
            # scripts:
            #   build:
            #     cmd: "echo {name}"
            #     cwd: "./app"
            #     env:
            #       FOO: "bar"
            cmd = entry.get('cmd') or entry.get('command') or ""
            cwd = entry.get('cwd')
            merge_env = entry.get('env', {}) if isinstance(
                entry.get('env', {}), dict) else {}
        else:
            logger.error(
                "Unrecognized script entry type for '%s'", script_name)
            return False

        if not isinstance(cmd, str) or not cmd.strip():
            logger.error("No command found for script '%s'", script_name)
            return False

        mapping = dict(os.environ)
        mapping.update({k: str(v) for k, v in params.items()})
        mapping.update({k: str(v) for k, v in merge_env.items()})

        cmd = self._safe_substitute(cmd, mapping)

        compiled_cmd, _compiled_files = self._auto_compile_prompts(cmd, params)

        run_env = dict(os.environ)
        run_env.update({k: str(v) for k, v in merge_env.items()})
        # Also expose provided params in env so scripts can access them as $KEY
        for k, v in params.items():
            if isinstance(k, str):
                # do not force upper case, maintain given key names
                run_env[k] = str(v)

        try:
            proc = subprocess.run(
                compiled_cmd,
                shell=True,
                cwd=cwd,
                env=run_env,
                check=False,
            )
            return proc.returncode == 0
        except Exception as exc:  # pragma: no cover
            logger.exception(
                "Failed executing script '%s': %s", script_name, exc)
            return False

    def list_scripts(self) -> Dict[str, str]:
        '''List all available scripts from apm.yml.
        Returns:
            Dict mapping script names to their commands
        '''
        config = self._load_config()
        if not config:
            return {}
        scripts = {}
        if isinstance(config, dict):
            raw_scripts = config.get('scripts', {})
            if isinstance(raw_scripts, dict):
                for name, val in raw_scripts.items():
                    scripts[name] = self._normalize_script_preview(val)
            # Consider top-level entries as possible scripts
            for k, v in config.items():
                if k == 'scripts':
                    continue
                if isinstance(v, (str, list, dict)):
                    scripts.setdefault(k, self._normalize_script_preview(v))
        return scripts

    def _load_config(self) -> Optional[Dict]:
        '''Load apm.yml from current directory.'''
        for fname in ("apm.yml", "apm.yaml"):
            path = Path(fname)
            if path.exists() and path.is_file():
                try:
                    if not yaml:
                        logger.error("PyYAML is required to parse %s", fname)
                        return None
                    with path.open("r", encoding="utf-8") as f:
                        data = yaml.safe_load(f) or {}
                        if isinstance(data, dict):
                            return data
                        logger.error("Invalid YAML format in %s", fname)
                        return None
                except Exception as exc:  # pragma: no cover
                    logger.exception("Failed to read %s: %s", fname, exc)
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
        # Identify .prompt.md occurrences regardless of quoting or --flag=path
        # We'll replace any occurrence of a path ending with .prompt.md that exists on disk.
        prompt_pattern = re.compile(
            r'(?P<path>[^\s\'"]+\.prompt\.md)\b', re.IGNORECASE)

        replacements: List[tuple[str, str]] = []
        compiled_outputs: List[str] = []

        def compile_one(p: str) -> Optional[tuple[str, str, str]]:
            path = Path(p)
            # Try also to resolve relative to current working directory
            if not path.exists():
                # Try POSIX normalization variant
                alt = Path(p.replace('\\', '/'))
                if alt.exists():
                    path = alt
            if not path.exists() or not path.is_file():
                return None
            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                return None
            compiled_content = self.compiler(text, params)
            compiled_path = path.with_suffix(".txt")
            try:
                compiled_path.write_text(compiled_content, encoding="utf-8")
            except Exception:  # pragma: no cover
                logger.exception(
                    "Failed to write compiled prompt to %s", str(compiled_path))
                return None
            return (str(path), compiled_content, str(compiled_path))

        # We will iterate over unique matches to avoid recompiling the same file multiple times
        unique_paths = []
        for m in prompt_pattern.finditer(command):
            p = m.group("path")
            if p not in unique_paths:
                unique_paths.append(p)

        compiled_command = command
        for p in unique_paths:
            result = compile_one(p)
            if not result:
                continue
            original_path, compiled_content, compiled_path = result
            compiled_outputs.append(compiled_path)
            transformed = self._transform_runtime_command(
                compiled_command, original_path, compiled_content, compiled_path
            )
            compiled_command = transformed

            # Also replace alternative path separators if present in the original command
            # e.g., replace backslash and posix variants
            alt_originals = set()
            alt_originals.add(original_path)
            try:
                alt_originals.add(Path(original_path).as_posix())
            except Exception:
                pass
            for alt in alt_originals:
                if alt != original_path:
                    compiled_command = compiled_command.replace(
                        alt, compiled_path)

        return compiled_command, compiled_outputs

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
        # Basic behavior: replace any occurrence of the prompt_file with the compiled .txt file path.
        # Also replace --prompt-file=... or --prompt=... patterns.
        # Keep quotes as-is by only replacing the internal path.
        escaped = re.escape(prompt_file)
        replaced = re.sub(escaped, compiled_path, command)

        # Replace common flag patterns that might include the extension explicitly
        patterns = [
            r'(--prompt(?:-file)?=)([^\s\'"]*\.prompt\.md)\b',
            r'(-p\s+)([^\s\'"]*\.prompt\.md)\b',
        ]
        for pat in patterns:
            replaced = re.sub(pat, lambda m: m.group(
                1) + compiled_path, replaced, flags=re.IGNORECASE)

        return replaced

    # Helpers

    @staticmethod
    def _normalize_script_preview(v) -> str:
        if isinstance(v, str):
            return v.strip().splitlines()[0] if v.strip() else ""
        if isinstance(v, list):
            return " && ".join([str(x) for x in v])
        if isinstance(v, dict):
            cmd = v.get('cmd') or v.get('command') or ""
            return str(cmd)
        return str(v)

    @staticmethod
    def _safe_substitute(text: str, mapping: Dict[str, str]) -> str:
        # First handle ${VAR} and $VAR style expansions
        def dollar_sub(m):
            key = m.group('key') or m.group('key2')
            return str(mapping.get(key, m.group(0)))

        text = re.sub(
            r'\$\{(?P<key>[A-Za-z_][A-Za-z0-9_]*)\}', dollar_sub, text)
        text = re.sub(r'\$(?P<key2>[A-Za-z_][A-Za-z0-9_]*)', dollar_sub, text)

        # Then handle {var} style expansions
        def brace_sub(m):
            key = m.group('key')
            return str(mapping.get(key, m.group(0)))

        text = re.sub(r'\{(?P<key>[A-Za-z_][A-Za-z0-9_]*)\}', brace_sub, text)
        return text

    def _default_compiler(self, markdown: str, params: Dict[str, str]) -> str:
        # Minimal "compilation": parameter substitution and normalize newlines.
        compiled = self._safe_substitute(
            markdown, {k: str(v) for k, v in params.items()})
        return compiled.strip() + ("\n" if not compiled.endswith("\n") else "")
