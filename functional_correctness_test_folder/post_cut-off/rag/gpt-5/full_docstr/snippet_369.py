from typing import Dict, Optional, Tuple, List
import os
import re
import shlex
import subprocess
from pathlib import Path

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None  # type: ignore


class _SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'


class ScriptRunner:
    '''Executes APM scripts with auto-compilation of .prompt.md files.'''

    def __init__(self, compiler=None):
        '''Initialize script runner with optional compiler.'''
        self.compiler = compiler

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        '''Run a script from apm.yml with parameter substitution.
        Args:
            script_name: Name of the script to run
            params: Parameters for compilation and script execution
        Returns:
            bool: True if script executed successfully
        '''
        try:
            cfg = self._load_config()
            if not cfg:
                return False
            scripts = cfg.get('scripts', {})
            if script_name not in scripts:
                return False
            command_value = scripts[script_name]
            command = self._coerce_command_to_string(command_value)
            # Parameter substitution for command
            command = command.format_map(_SafeDict(params or {}))
            # Auto-compile prompt files and transform command
            command, _compiled_files = self._auto_compile_prompts(
                command, params or {})
            # Prepare environment
            env = os.environ.copy()
            for k, v in (params or {}).items():
                if isinstance(v, (str, bytes)):
                    env[str(k)] = v.decode() if isinstance(v, bytes) else v
                else:
                    env[str(k)] = str(v)
            # Execute
            completed = subprocess.run(command, shell=True, env=env)
            return completed.returncode == 0
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
        scripts = cfg.get('scripts', {}) or {}
        out: Dict[str, str] = {}
        for k, v in scripts.items():
            out[k] = self._coerce_command_to_string(v)
        return out

    def _load_config(self) -> Optional[Dict]:
        '''Load apm.yml from current directory.'''
        try:
            cwd = Path.cwd()
            candidates = [cwd / 'apm.yml', cwd / 'apm.yaml']
            apm_path = next((p for p in candidates if p.exists()), None)
            if not apm_path or yaml is None:
                return None
            with open(apm_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
            if not isinstance(data, dict):
                return None
            return data
        except Exception:
            return None

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> Tuple[str, List[str]]:
        '''Auto-compile .prompt.md files and transform runtime commands.
        Args:
            command: Original script command
            params: Parameters for compilation
        Returns:
            Tuple of (compiled_command, list_of_compiled_prompt_files)
        '''
        tokens = self._split_shell_preserve_quotes(command)
        prompt_tokens: List[str] = []
        for tok in tokens:
            # Remove surrounding quotes for detection
            unquoted = tok[1:-1] if (len(tok) >= 2 and ((tok[0]
                                     == tok[-1]) and tok[0] in ("'", '"'))) else tok
            if unquoted.endswith('.prompt.md'):
                prompt_tokens.append(unquoted)

        compiled_files: List[str] = []
        transformed_command = command
        seen: set = set()

        for prompt_path in prompt_tokens:
            if prompt_path in seen:
                continue
            seen.add(prompt_path)
            compiled_content, compiled_path = self._compile_prompt_file(
                prompt_path, params)
            compiled_files.append(compiled_path)
            transformed_command = self._transform_runtime_command(
                transformed_command, prompt_path, compiled_content, compiled_path
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
        # Replace occurrences of the prompt file path (with or without quotes) to compiled path
        # Build regex to match prompt_file possibly wrapped in single/double quotes
        escaped = re.escape(prompt_file)
        pattern = rf'(?P<q>["\'])?{escaped}(?P=q)?'

        def _repl(m):
            q = m.group('q')
            if q:
                return f'{q}{compiled_path}{q}'
            return compiled_path
        return re.sub(pattern, _repl, command)

    def _compile_prompt_file(self, prompt_path: str, params: Dict[str, str]) -> Tuple[str, str]:
        # Resolve path
        src_path = Path(prompt_path).expanduser().resolve()
        if not src_path.exists():
            raise FileNotFoundError(f'Prompt file not found: {src_path}')

        # Decide compiled output path inside a hidden build dir next to source
        out_dir = src_path.parent / '.apm_build'
        out_dir.mkdir(parents=True, exist_ok=True)
        out_name = src_path.name.replace('.prompt.md', '.txt')
        compiled_path = str((out_dir / out_name).resolve())

        # Compile content
        text = src_path.read_text(encoding='utf-8')
        compiled_content = self._do_compile(text, str(src_path), params)

        # Write compiled
        with open(compiled_path, 'w', encoding='utf-8') as f:
            f.write(compiled_content if compiled_content.endswith(
                '\n') else compiled_content + '\n')

        return compiled_content, compiled_path

    def _do_compile(self, text: str, source_path: str, params: Dict[str, str]) -> str:
        # Prefer compiler.compile_file if available
        try:
            if self.compiler is not None:
                if hasattr(self.compiler, 'compile_file') and callable(getattr(self.compiler, 'compile_file')):
                    return str(self.compiler.compile_file(source_path, params))
                if hasattr(self.compiler, 'compile') and callable(getattr(self.compiler, 'compile')):
                    return str(self.compiler.compile(text, params))
        except Exception:
            pass
        # Fallback: simple format-based substitution
        try:
            return text.format_map(_SafeDict(params or {}))
        except Exception:
            return text

    def _coerce_command_to_string(self, value) -> str:
        if isinstance(value, str):
            return value
        if isinstance(value, list):
            return ' && '.join(str(x) for x in value)
        if isinstance(value, dict) and 'cmd' in value:
            return str(value['cmd'])
        return str(value)

    def _split_shell_preserve_quotes(self, command: str) -> List[str]:
        try:
            return shlex.split(command)
        except Exception:
            # Fallback naive split
            return command.split()
