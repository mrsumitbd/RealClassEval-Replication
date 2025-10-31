from typing import Dict, Optional, List
import os
import subprocess
import shlex
from pathlib import Path
from string import Template

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None


class _SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'


class ScriptRunner:
    '''Executes APM scripts with auto-compilation of .prompt.md files.'''

    def __init__(self, compiler=None):
        '''Initialize script runner with optional compiler.'''
        self.compiler = compiler
        self._config_cache: Optional[Dict] = None
        self._compiled_dir = Path('.apm_compiled')
        self._compiled_dir.mkdir(parents=True, exist_ok=True)

    def run_script(self, script_name: str, params: Dict[str, str]) -> bool:
        '''Run a script from apm.yml with parameter substitution.
        Args:
            script_name: Name of the script to run
            params: Parameters for compilation and script execution
        Returns:
            bool: True if script executed successfully
        '''
        scripts = self.list_scripts()
        command = scripts.get(script_name)
        if not command:
            return False

        compiled_command, _ = self._auto_compile_prompts(command, params)
        compiled_command = self._substitute_params(compiled_command, params)

        env = os.environ.copy()
        for k, v in params.items():
            env[f'APM_{str(k).upper()}'] = str(v)

        proc = subprocess.run(compiled_command, shell=True, env=env)
        return proc.returncode == 0

    def list_scripts(self) -> Dict[str, str]:
        '''List all available scripts from apm.yml.
        Returns:
            Dict mapping script names to their commands
        '''
        cfg = self._load_config()
        if not cfg:
            return {}
        scripts_section = None
        if isinstance(cfg, dict) and 'scripts' in cfg and isinstance(cfg['scripts'], dict):
            scripts_section = cfg['scripts']
        elif isinstance(cfg, dict):
            scripts_section = cfg
        else:
            return {}

        scripts: Dict[str, str] = {}
        for name, value in scripts_section.items():
            if isinstance(value, list):
                scripts[name] = ' && '.join(map(str, value))
            else:
                scripts[name] = str(value)
        return scripts

    def _load_config(self) -> Optional[Dict]:
        '''Load apm.yml from current directory.'''
        if self._config_cache is not None:
            return self._config_cache
        for fname in ('apm.yml', 'apm.yaml'):
            p = Path.cwd() / fname
            if p.exists():
                if not yaml:
                    return None
                with p.open('r', encoding='utf-8') as f:
                    self._config_cache = yaml.safe_load(f) or {}
                    return self._config_cache
        self._config_cache = None
        return None

    def _auto_compile_prompts(self, command: str, params: Dict[str, str]) -> tuple[str, list[str]]:
        '''Auto-compile .prompt.md files and transform runtime commands.
        Args:
            command: Original script command
            params: Parameters for compilation
        Returns:
            Tuple of (compiled_command, list_of_compiled_prompt_files)
        '''
        try:
            tokens = shlex.split(command, posix=True)
        except Exception:
            tokens = command.split()

        # Collect candidate prompt files from tokens
        prompt_tokens: List[str] = []
        for i, tok in enumerate(tokens):
            candidate = tok
            if candidate.startswith('@'):
                candidate = candidate[1:]
            if candidate.endswith('.prompt.md'):
                prompt_tokens.append(tok)
            # redirection case: "< file.prompt.md"
            if tok == '<' and i + 1 < len(tokens):
                nxt = tokens[i + 1]
                if nxt.endswith('.prompt.md'):
                    prompt_tokens.append(nxt)

        compiled_files: List[str] = []
        transformed_command = command
        compiled_cache: Dict[str, str] = {}

        for tok in prompt_tokens:
            original_token = tok
            prompt_path_str = tok[1:] if tok.startswith('@') else tok
            prompt_path = Path(prompt_path_str)
            if not prompt_path.exists():
                # If path not found, skip compilation but still attempt transform for consistency
                compiled_content = ''
            else:
                compiled_content = self._compile_prompt_file(
                    prompt_path, params)

            compiled_path = self._compiled_dir / \
                prompt_path.name.replace('.prompt.md', '.txt')
            compiled_path.parent.mkdir(parents=True, exist_ok=True)
            compiled_path.write_text(compiled_content, encoding='utf-8')
            compiled_files.append(str(compiled_path))

            # Cache compiled path for any duplicates
            compiled_cache[original_token] = str(compiled_path)

            transformed_command = self._transform_runtime_command(
                transformed_command,
                prompt_file=prompt_path_str,
                compiled_content=compiled_content,
                compiled_path=str(compiled_path),
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
        try:
            tokens = shlex.split(command, posix=True)
        except Exception:
            tokens = command.split()

        new_tokens: List[str] = []
        i = 0
        while i < len(tokens):
            tok = tokens[i]
            # Replace direct token match
            base = tok[1:] if tok.startswith('@') else tok
            if base == prompt_file:
                replacement = '@' + \
                    compiled_path if tok.startswith('@') else compiled_path
                new_tokens.append(replacement)
                i += 1
                continue
            # Replace redirection case: "< prompt_file"
            if tok == '<' and i + 1 < len(tokens):
                nxt = tokens[i + 1]
                if nxt == prompt_file:
                    new_tokens.extend(['<', compiled_path])
                    i += 2
                    continue
            new_tokens.append(tok)
            i += 1

        # Reconstruct command safely
        try:
            # Python 3.8+: shlex.join exists
            join = shlex.join  # type: ignore[attr-defined]
        except AttributeError:  # pragma: no cover
            def join(parts: List[str]) -> str:
                return ' '.join(shlex.quote(p) for p in parts)

        return join(new_tokens)

    def _substitute_params(self, command: str, params: Dict[str, str]) -> str:
        # 1) ${var} style
        substituted = Template(command).safe_substitute(
            {k: str(v) for k, v in params.items()})
        # 2) {var} style
        substituted = substituted.format_map(
            _SafeDict({k: str(v) for k, v in params.items()}))
        return substituted

    def _compile_prompt_file(self, prompt_path: Path, params: Dict[str, str]) -> str:
        content = prompt_path.read_text(encoding='utf-8')
        if self.compiler:
            # Support various compiler interfaces
            if hasattr(self.compiler, 'compile_file') and callable(self.compiler.compile_file):
                try:
                    return self.compiler.compile_file(str(prompt_path), params)
                except TypeError:
                    return self.compiler.compile_file(str(prompt_path))
            if hasattr(self.compiler, 'compile') and callable(self.compiler.compile):
                # type: ignore[call-arg]
                return self.compiler.compile(content, params)
        # Fallback: simple variable substitution on file content
        text = Template(content).safe_substitute(
            {k: str(v) for k, v in params.items()})
        text = text.format_map(
            _SafeDict({k: str(v) for k, v in params.items()}))
        return text
