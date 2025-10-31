import os
import json
import shlex
from typing import Any, Dict, Optional, List


class MCPConfigGenerator:
    '''Generator for MCP server configuration.'''

    def __init__(self, base_dir: Optional[str] = None):
        '''
        Initialize the MCP config generator.
        Args:
            base_dir: Base directory for resolving relative paths (defaults to current working directory)
        '''
        self.base_dir = os.path.abspath(base_dir or os.getcwd())

    def _expand(self, value: str) -> str:
        if not isinstance(value, str):
            return value
        return os.path.expanduser(os.path.expandvars(value))

    def _resolve_path(self, value: str) -> str:
        expanded = self._expand(value)
        if os.path.isabs(expanded):
            return os.path.normpath(expanded)
        return os.path.normpath(os.path.join(self.base_dir, expanded))

    def _is_pathlike(self, value: str) -> bool:
        if not isinstance(value, str):
            return False
        return any([
            os.sep in value,
            (os.altsep in value) if os.altsep else False,
            value.startswith(('.', '~')),
        ])

    def _normalize_args(self, args: Any) -> List[str]:
        if args is None:
            return []
        if isinstance(args, str):
            parts = shlex.split(args)
        elif isinstance(args, (list, tuple)):
            parts = list(args)
        else:
            raise ValueError("args must be a string or list/tuple of strings")
        norm: List[str] = []
        for a in parts:
            a_str = str(a)
            a_exp = self._expand(a_str)
            if self._is_pathlike(a_exp):
                try:
                    norm.append(self._resolve_path(a_exp))
                except Exception:
                    norm.append(a_exp)
            else:
                norm.append(a_exp)
        return norm

    def _normalize_env(self, global_env: Dict[str, Any], local_env: Optional[Dict[str, Any]]) -> Dict[str, str]:
        env: Dict[str, str] = {}
        if global_env:
            for k, v in global_env.items():
                if v is None:
                    continue
                env[str(k)] = self._expand(str(v))
        if local_env:
            for k, v in local_env.items():
                k_s = str(k)
                if v is None:
                    if k_s in env:
                        env.pop(k_s, None)
                    continue
                env[k_s] = self._expand(str(v))
        return env

    def _normalize_server_entry(self, name: str, server_cfg: Dict[str, Any], global_env: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        enabled = server_cfg.get('enabled', True)
        if enabled is False:
            return None

        command = server_cfg.get('command') or server_cfg.get(
            'cmd') or server_cfg.get('executable')
        if not command or not isinstance(command, str):
            raise ValueError(
                f"Server '{name}': missing required 'command' (string)")

        args = self._normalize_args(server_cfg.get('args'))
        cwd = server_cfg.get('cwd')
        transport = server_cfg.get('transport')

        # Resolve command if path-like; leave bare executables alone (e.g., 'python')
        command_expanded = self._expand(command)
        command_final = self._resolve_path(command_expanded) if self._is_pathlike(
            command_expanded) else command_expanded

        entry: Dict[str, Any] = {'command': command_final}
        if args:
            entry['args'] = args
        if cwd:
            entry['cwd'] = self._resolve_path(str(cwd))
        env = self._normalize_env(global_env, server_cfg.get('env'))
        if env:
            entry['env'] = env
        if transport:
            entry['transport'] = transport

        return entry

    def _normalize_servers_collection(self, servers: Any) -> Dict[str, Dict[str, Any]]:
        if isinstance(servers, dict):
            # Could be mapping name -> config
            return {str(name): cfg for name, cfg in servers.items()}
        if isinstance(servers, list):
            result: Dict[str, Dict[str, Any]] = {}
            for idx, item in enumerate(servers):
                if not isinstance(item, dict):
                    raise ValueError(f"servers[{idx}] must be a dict")
                name = item.get('name') or item.get('id')
                if not name:
                    raise ValueError(f"servers[{idx}] missing required 'name'")
                name_s = str(name)
                result[name_s] = item
            return result
        raise ValueError("config['servers'] must be a list or dict")

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Generate a full MCP server configuration from a simplified config.
        Args:
            config: Simplified configuration dictionary
        Returns:
            Complete MCP server configuration
        '''
        if not isinstance(config, dict):
            raise ValueError("config must be a dict")

        if 'mcpServers' in config and 'servers' not in config:
            # Already in final shape; still perform minimal normalization on env/cwd/args/command
            final = {'mcpServers': {}}
            global_env = config.get('env', {}) if isinstance(
                config.get('env', {}), dict) else {}
            for name, srv in config['mcpServers'].items():
                if not isinstance(srv, dict):
                    continue
                # Treat these as normalized entries; only expand/resolve where applicable
                s: Dict[str, Any] = dict(srv)
                if 'command' in s and isinstance(s['command'], str):
                    cmd = self._expand(s['command'])
                    s['command'] = self._resolve_path(
                        cmd) if self._is_pathlike(cmd) else cmd
                if 'args' in s:
                    s['args'] = self._normalize_args(s.get('args'))
                if 'cwd' in s and isinstance(s['cwd'], str):
                    s['cwd'] = self._resolve_path(s['cwd'])
                env = self._normalize_env(global_env, s.get(
                    'env') if isinstance(s.get('env'), dict) else {})
                if env:
                    s['env'] = env
                elif 'env' in s:
                    s.pop('env', None)
                enabled = s.get('enabled', True)
                if enabled is False:
                    continue
                s.pop('enabled', None)
                final['mcpServers'][str(name)] = s
            if not final['mcpServers']:
                raise ValueError("No enabled servers found in mcpServers")
            return final

        servers_cfg = config.get('servers')
        if not servers_cfg:
            raise ValueError("config must contain 'servers'")

        servers_map = self._normalize_servers_collection(servers_cfg)
        global_env = config.get('env', {}) if isinstance(
            config.get('env', {}), dict) else {}

        mcp_servers: Dict[str, Any] = {}
        for name, srv_cfg in servers_map.items():
            if not isinstance(srv_cfg, dict):
                raise ValueError(f"Server '{name}' config must be a dict")
            normalized = self._normalize_server_entry(
                name, srv_cfg, global_env)
            if normalized is not None:
                mcp_servers[name] = normalized

        if not mcp_servers:
            raise ValueError("No enabled servers to generate configuration")

        return {'mcpServers': mcp_servers}

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        '''
        Write the generated configuration to a file.
        Args:
            config: The simplified configuration dictionary
            output_path: Path to write the generated configuration
        '''
        final_cfg = self.generate_config(config)

        out_dir = os.path.dirname(os.path.abspath(output_path)) or '.'
        os.makedirs(out_dir, exist_ok=True)

        ext = os.path.splitext(output_path)[1].lower()
        if ext in ('.yaml', '.yml'):
            try:
                import yaml  # type: ignore
            except Exception as e:
                raise ValueError(
                    "PyYAML is required to write YAML files. Install with 'pip install pyyaml'.") from e
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(final_cfg, f, sort_keys=True)
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(final_cfg, f, indent=2,
                          ensure_ascii=False, sort_keys=True)
