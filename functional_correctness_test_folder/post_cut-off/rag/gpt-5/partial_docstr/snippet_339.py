import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional


class MCPConfigGenerator:
    '''Generator for MCP server configuration.'''

    def __init__(self, base_dir: Optional[str] = None):
        '''
        Initialize the MCP config generator.
        Args:
            base_dir: Base directory for resolving relative paths (defaults to current working directory)
        '''
        self.base_dir = Path(base_dir).expanduser(
        ).resolve() if base_dir else Path.cwd()

    def _resolve_path(self, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        p = Path(os.path.expandvars(os.path.expanduser(str(value))))
        if not p.is_absolute():
            p = self.base_dir / p
        try:
            return str(p.resolve())
        except Exception:
            return str(p)

    def _venv_python(self, venv_path: str) -> str:
        venv = Path(self._resolve_path(venv_path))
        if os.name == 'nt':
            candidate = venv / 'Scripts' / 'python.exe'
        else:
            candidate = venv / 'bin' / 'python'
        return str(candidate)

    def _merge_env(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, str]:
        merged: Dict[str, str] = {}
        for k, v in (base or {}).items():
            merged[str(k)] = '' if v is None else str(v)
        for k, v in (override or {}).items():
            merged[str(k)] = '' if v is None else str(v)
        return merged

    def _transport_from_spec(self, spec: Dict[str, Any], defaults: Dict[str, Any]) -> Dict[str, Any]:
        if 'transport' in spec and isinstance(spec['transport'], dict):
            t = dict(spec['transport'])
            if 'type' not in t:
                t['type'] = 'stdio'
            return t
        if 'sse' in spec and isinstance(spec['sse'], dict):
            sse = spec['sse']
            t: Dict[str, Any] = {'type': 'sse', 'url': sse.get('url')}
            if 'headers' in sse and isinstance(sse['headers'], dict):
                t['headers'] = {str(k): str(v)
                                for k, v in sse['headers'].items()}
            return t
        if 'stdio' in spec:
            if isinstance(spec['stdio'], dict):
                t = dict(spec['stdio'])
                t.setdefault('type', 'stdio')
                return t
            if spec['stdio'] is False:
                # placeholder if user disables stdio without sse provided
                return {'type': 'sse'}
        if 'transport' in defaults and isinstance(defaults['transport'], dict):
            t = dict(defaults['transport'])
            t.setdefault('type', 'stdio')
            return t
        return {'type': 'stdio'}

    def _command_from_spec(self, name: str, spec: Dict[str, Any]) -> (str, list):
        # Python module execution support
        if 'python' in spec and isinstance(spec['python'], dict):
            py = spec['python']
            module = py.get('module')
            if not module:
                raise ValueError(
                    f"Server '{name}' python specification requires a 'module'")
            python_exe = py.get('python_path')
            if not python_exe and py.get('venv'):
                python_exe = self._venv_python(py['venv'])
            if not python_exe:
                python_exe = sys.executable
            args = ['-m', module]
            if isinstance(py.get('args'), list):
                args.extend([str(a) for a in py['args']])
            if isinstance(spec.get('args'), list):
                args.extend([str(a) for a in spec['args']])
            return str(self._resolve_path(python_exe)), args

        # Direct command/path execution
        command = spec.get('command') or spec.get('path')
        if not command:
            raise ValueError(
                f"Server '{name}' requires a 'command', 'path', or 'python' specification")
        args = [str(a) for a in spec.get('args') or []]
        return str(command), args

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Generate a full MCP server configuration from a simplified config.
        Args:
            config: Simplified configuration dictionary
        Returns:
            Complete MCP server configuration
        '''
        if not isinstance(config, dict):
            raise TypeError('config must be a dict')
        servers = config.get('servers') or config.get('mcpServers')
        if not isinstance(servers, dict) or not servers:
            raise ValueError(
                "config must contain a non-empty 'servers' or 'mcpServers' dict")

        defaults = config.get('defaults') or {}
        out: Dict[str, Any] = {'version': config.get(
            'version', 1), 'mcpServers': {}}

        default_env = defaults.get('env') if isinstance(
            defaults.get('env'), dict) else {}
        default_cwd = defaults.get('cwd')

        for name, spec in servers.items():
            if not isinstance(spec, dict):
                raise ValueError(f"Server '{name}' spec must be a dict")
            if spec.get('enabled') is False:
                continue

            command, args = self._command_from_spec(name, spec)

            env = self._merge_env(default_env, spec.get('env') or {})
            cwd = spec.get('cwd', default_cwd)
            cwd_resolved = self._resolve_path(cwd) if cwd else None

            transport = self._transport_from_spec(spec, defaults)

            entry: Dict[str, Any] = {
                'command': command,
                'args': args,
                'transport': transport
            }
            if env:
                entry['env'] = env
            if cwd_resolved:
                entry['cwd'] = cwd_resolved

            out['mcpServers'][str(name)] = entry

        return out

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        '''
        Write the generated configuration to a file.
        Args:
            config: The simplified configuration dictionary
            output_path: Path to write the generated configuration
        '''
        generated = self.generate_config(config)
        output = Path(output_path).expanduser()
        if not output.parent.exists():
            output.parent.mkdir(parents=True, exist_ok=True)

        ext = output.suffix.lower()
        if ext in ('.yaml', '.yml'):
            try:
                import yaml  # type: ignore
                with output.open('w', encoding='utf-8') as f:
                    yaml.safe_dump(generated, f, sort_keys=False,
                                   allow_unicode=True)
                return
            except Exception:
                pass
        with output.open('w', encoding='utf-8') as f:
            json.dump(generated, f, indent=2,
                      ensure_ascii=False, sort_keys=False)
