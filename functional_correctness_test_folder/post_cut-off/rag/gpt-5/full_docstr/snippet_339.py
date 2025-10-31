import os
import json
from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple, Union


class MCPConfigGenerator:
    '''Generator for MCP server configuration.'''

    def __init__(self, base_dir: Optional[str] = None):
        '''
        Initialize the MCP config generator.
        Args:
            base_dir: Base directory for resolving relative paths (defaults to current working directory)
        '''
        self.base_dir = os.path.abspath(base_dir or os.getcwd())

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Generate a full MCP server configuration from a simplified config.
        Args:
            config: Simplified configuration dictionary
        Returns:
            Complete MCP server configuration
        '''
        if not isinstance(config, dict):
            raise ValueError('config must be a dictionary')

        cfg = deepcopy(config)

        variables = cfg.get('variables', {}) or {}
        variables = {**variables, 'BASE_DIR': self.base_dir}

        global_env = cfg.get('env', {}) or cfg.get('global_env', {}) or {}

        mcp_servers_input = cfg.get('servers') or cfg.get('mcpServers')
        if not mcp_servers_input:
            raise ValueError(
                "config must contain 'servers' (list or dict) or 'mcpServers' (dict)")

        servers_iter: List[Tuple[str, Dict[str, Any]]]
        if isinstance(mcp_servers_input, dict):
            servers_iter = list(mcp_servers_input.items())
        elif isinstance(mcp_servers_input, list):
            servers_iter = []
            for idx, item in enumerate(mcp_servers_input):
                if not isinstance(item, dict):
                    raise ValueError(f"servers[{idx}] must be a dict")
                name = item.get('name') or item.get('id')
                if not name:
                    raise ValueError(f"servers[{idx}] must include 'name'")
                servers_iter.append((name, item))
        else:
            raise ValueError(
                "'servers' or 'mcpServers' must be a list or dict")

        result: Dict[str, Any] = {'mcpServers': {}}

        for name, spec in servers_iter:
            if not isinstance(spec, dict):
                raise ValueError(f"Server '{name}' spec must be a dict")
            spec = deepcopy(spec)

            enabled = spec.get('enabled', True)
            disabled = not bool(enabled)

            description = spec.get('description')

            # Expand and resolve cwd
            cwd = spec.get('cwd')
            cwd = self._resolve_path(self._expand_vars(
                cwd, variables), allow_none=True)

            # Merge env: global first, then server-specific
            server_env = spec.get('env', {}) or {}
            merged_env = {**global_env, **server_env}
            merged_env = self._expand_vars(
                merged_env, variables) if merged_env else None

            # Build command block if present
            command_block = None
            if 'command' in spec or 'args' in spec or 'path' in spec:
                command_block = self._build_command_block(spec, variables, cwd)

                # Merge env/cwd into command block
                if merged_env:
                    command_block['env'] = merged_env
                if cwd:
                    command_block['cwd'] = cwd

            # Build transport block
            transport_block = None
            if 'transport' in spec and isinstance(spec['transport'], dict):
                transport_block = self._expand_vars(
                    spec['transport'], variables)
            else:
                transport_type = (spec.get('type') or spec.get(
                    'transport_type') or 'stdio').lower()
                transport_block = self._build_transport_block(
                    transport_type, spec, variables)

            server_entry: Dict[str, Any] = {}
            if command_block:
                server_entry['command'] = command_block
            if transport_block:
                server_entry['transport'] = transport_block
            server_entry['disabled'] = disabled
            if description:
                server_entry['description'] = self._expand_vars(
                    description, variables)

            result['mcpServers'][name] = server_entry

        return result

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        '''
        Write the generated configuration to a file.
        Args:
            config: The simplified configuration dictionary
            output_path: Path to write the generated configuration
        '''
        generated = self.generate_config(config)
        output_path = os.path.abspath(self._expand_vars(
            output_path, {'BASE_DIR': self.base_dir}))
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        lower = output_path.lower()
        if lower.endswith('.json'):
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(generated, f, indent=2, ensure_ascii=False)
        elif lower.endswith('.yml') or lower.endswith('.yaml'):
            try:
                import yaml  # type: ignore
            except Exception:
                # Fallback to JSON if PyYAML isn't available
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(generated, f, indent=2, ensure_ascii=False)
            else:
                with open(output_path, 'w', encoding='utf-8') as f:
                    yaml.safe_dump(generated, f, sort_keys=False)
        else:
            # Default to JSON
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(generated, f, indent=2, ensure_ascii=False)

    # Internal helpers

    def _build_command_block(self, spec: Dict[str, Any], variables: Dict[str, Any], cwd: Optional[str]) -> Dict[str, Any]:
        command = spec.get('command')
        args = spec.get('args')
        path = spec.get('path')

        # Normalize command specification
        cmd_path: Optional[str] = None
        cmd_args: List[str] = []

        if isinstance(command, list):
            if not command:
                raise ValueError(
                    "When 'command' is a list, it must contain at least one element (executable)")
            # The first element is the executable path; the rest are args
            cmd_path = self._resolve_path(self._expand_vars(
                command[0], variables), allow_none=True)
            cmd_args = [self._expand_vars(a, variables) for a in command[1:]]
        elif isinstance(command, str):
            cmd_path = self._resolve_path(self._expand_vars(
                command, variables), allow_none=True)
        elif command is None:
            if isinstance(path, str):
                cmd_path = self._resolve_path(
                    self._expand_vars(path, variables), allow_none=True)

        if args:
            if not isinstance(args, list):
                raise ValueError("'args' must be a list of strings")
            cmd_args.extend([self._expand_vars(a, variables) for a in args])

        block: Dict[str, Any] = {}
        if cmd_path:
            block['path'] = cmd_path
        if cmd_args:
            block['args'] = cmd_args
        if cwd:
            block['cwd'] = cwd
        return block

    def _build_transport_block(self, transport_type: str, spec: Dict[str, Any], variables: Dict[str, Any]) -> Dict[str, Any]:
        # If url is given, use it directly; otherwise construct from host/port/path
        def build_url(default_scheme: str) -> Optional[str]:
            url = spec.get('url')
            if url:
                return self._expand_vars(url, variables)
            host = spec.get('host', 'localhost')
            port = spec.get('port')
            path = spec.get('path', '')
            tls = bool(spec.get('tls') or spec.get('secure'))
            scheme = default_scheme + ('s' if tls else '')
            if port is None:
                # If no port specified, do not add it to the URL
                return f"{scheme}://{host}{path if path.startswith('/') else f'/{path}' if path else ''}"
            return f"{scheme}://{host}:{port}{path if path.startswith('/') else f'/{path}' if path else ''}"

        transport_type = (transport_type or 'stdio').lower()
        if transport_type == 'stdio':
            return {'stdio': {}}
        if transport_type in ('sse', 'eventsource', 'event-stream'):
            url = build_url('http')
            if not url:
                raise ValueError(
                    "SSE transport requires a 'url' or host/port/path")
            return {'sse': {'url': url}}
        if transport_type in ('ws', 'wss', 'websocket'):
            url = build_url('ws')
            if not url:
                raise ValueError(
                    "WebSocket transport requires a 'url' or host/port/path")
            return {'websocket': {'url': url}}
        # Pass-through if custom transport provided
        custom = spec.get('transport')
        if isinstance(custom, dict):
            return self._expand_vars(custom, variables)
        raise ValueError(f"Unsupported transport type '{transport_type}'")

    def _expand_vars(self, value: Any, variables: Dict[str, Any]) -> Any:
        if value is None:
            return None
        if isinstance(value, str):
            # env-style expansion
            expanded = os.path.expandvars(value)
            # format-style expansion with provided variables
            try:
                expanded = expanded.format(**variables)
            except Exception:
                # ignore formatting errors to avoid surprising failures
                pass
            return expanded
        if isinstance(value, list):
            return [self._expand_vars(v, variables) for v in value]
        if isinstance(value, dict):
            return {k: self._expand_vars(v, variables) for k, v in value.items()}
        return value

    def _resolve_path(self, path: Optional[str], allow_none: bool = False) -> Optional[str]:
        if path is None:
            return None if allow_none else ''
        # Expand ~ and env vars first
        path = os.path.expanduser(os.path.expandvars(path))
        if os.path.isabs(path):
            return path
        return os.path.abspath(os.path.join(self.base_dir, path))
