from typing import Dict, Optional, List
import os
import re
import shlex
import subprocess
from pathlib import Path

try:
    import yaml  # type: ignore
except Exception:
    yaml = None


class ScriptRunner:
    '''Executes APM scripts with auto-compilation of .prompt.md files.'''

    def __init__(self, compiler=None):
        '''Initialize script runner with optional compiler.'''
        self.compiler = compiler
        self._config_cache: Optional[Dict] = None
        self.compiled_root = Path('.apm') / 'compiled'

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

        scripts = self.list_scripts()
        if script_name not in scripts:
            return False

        raw_command = scripts[script_name]
        substituted_command = self._substitute_params(raw_command, params)
        compiled_command, _ = self._auto_compile_prompts(
            substituted_command, params)

        env = os.environ.copy()
        for k, v in (params or {}).items():
            if isinstance(k, str) and isinstance(v, (str, int, float, bool)):
                env[k] = str(v)

        try:
            completed = subprocess.run(compiled_command, shell=True, env=env)
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
        if isinstance(config, dict):
            if 'scripts' in config and isinstance(config['scripts'], dict):
                # normalize to str command
                return {k: str(v) for k, v in config['scripts'].items()}
            # fallback: treat top-level as scripts if values are strings
            str_values = {k: v for k,
                          v in config.items() if isinstance(v, str)}
            if str_values:
                return str_values
        return {}

    def _load_config(self) -> Optional[Dict]:
        '''Load apm.yml from current directory.'''
        if self._config_cache is not None:
            return self._config_cache
        if yaml is None:
            return None
        for fname in ('apm.yml', 'apm.yaml'):
            p = Path.cwd() / fname
            if p.exists():
                try:
                    with p.open('r', encoding='utf-8') as f:
                        data = yaml.safe_load(f) or {}
                        if isinstance(data, dict):
                            self._config_cache = data
                            return data
                        else:
                            self._config_cache = {}
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
        tokens = self._safe_shlex_split(command)
        compiled_files: List[str] = []
        seen: set[str] = set()

        # Ensure compiled root exists
        self.compiled_root.mkdir(parents=True, exist_ok=True)

        # Scan tokens to find .prompt.md references (standalone or prefixed with '@')
        # list of (original_reference_token, prompt_path_without_prefix)
        prompt_refs: List[tuple[str, str]] = []
        for tok in tokens:
            if tok.endswith('.prompt.md'):
                prompt_refs.append((tok, tok))
            elif tok.startswith('@') and tok[1:].endswith('.prompt.md'):
                prompt_refs.append((tok, tok[1:]))

        updated_command = command
        for ref_token, prompt_path in prompt_refs:
            if prompt_path in seen:
                # still replace tokens consistently
                compiled_path = self._compiled_path_for(prompt_path)
                updated_command = self._transform_runtime_command(
                    updated_command, prompt_path, '', str(compiled_path))
                continue
            seen.add(prompt_path)

            compiled_content = self._compile_prompt_file(prompt_path, params)
            compiled_path = self._compiled_path_for(prompt_path)
            compiled_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                with compiled_path.open('w', encoding='utf-8') as f:
                    f.write(compiled_content)
            except Exception:
                # If unable to write, skip replacement for this prompt
                continue

            compiled_files.append(str(compiled_path))
            updated_command = self._transform_runtime_command(
                updated_command, prompt_path, compiled_content, str(compiled_path))

        return updated_command, compiled_files

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
        escaped = re.escape(prompt_file)
        # Replace quoted occurrences
        command = command.replace(f"'{prompt_file}'", f"'{compiled_path}'")
        command = command.replace(f'"{prompt_file}"', f'"{compiled_path}"')
        # Replace @file occurrences (e.g., curl -d @file)
        command = command.replace(f'@{prompt_file}', f'@{compiled_path}')
        # Replace bare token occurrences using conservative boundaries
        pattern = rf'(?<![\w@./-]){escaped}(?![\w./-])'
        command = re.sub(pattern, compiled_path, command)
        return command

    # Helpers

    def _substitute_params(self, text: str, params: Dict[str, str]) -> str:
        # {{var}} style
        def _mustache(m):
            key = m.group(1)
            return str(params.get(key, os.environ.get(key, '')))
        out = re.sub(
            r'\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}', _mustache, text)

        # {var} style
        class _SafeDict(dict):
            def __missing__(self, key):
                return os.environ.get(key, '')

        try:
            out = out.format_map(_SafeDict(**(params or {})))
        except Exception:
            pass

        # ${var} style
        try:
            import string
            tmpl = string.Template(out)
            out = tmpl.safe_substitute({**os.environ, **(params or {})})
        except Exception:
            pass

        return out

    def _compile_prompt_file(self, prompt_path: str, params: Dict[str, str]) -> str:
        # Try user-provided compiler
        compiler = self.compiler
        if compiler is not None:
            for method_name in ('compile_prompt', 'compile_file', 'compile'):
                fn = getattr(compiler, method_name, None)
                if callable(fn):
                    try:
                        result = fn(prompt_path, params)  # type: ignore
                        if isinstance(result, str) and result.strip() != '':
                            return result
                    except TypeError:
                        # Try without params
                        try:
                            result = fn(prompt_path)  # type: ignore
                            if isinstance(result, str) and result.strip() != '':
                                return result
                        except Exception:
                            pass
                    except Exception:
                        pass

        # Fallback: read file and substitute params
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            content = ''
        return self._substitute_params(content, params or {})

    def _compiled_path_for(self, prompt_path: str) -> Path:
        p = Path(prompt_path)
        rel: Path
        try:
            rel = p.relative_to(Path.cwd())
        except Exception:
            rel = Path(p.name)
        compiled_name = re.sub(r'\.prompt\.md$', '.txt', rel.name)
        return self.compiled_root / rel.parent / compiled_name

    def _safe_shlex_split(self, command: str) -> List[str]:
        try:
            return shlex.split(command, posix=True)
        except Exception:
            return command.split()
