from __future__ import annotations

import json
import os
import shlex
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

    def _resolve_path(self, p: Optional[str]) -> Optional[str]:
        if p is None:
            return None
        return str((self.base_dir / Path(os.path.expandvars(os.path.expanduser(p)))).resolve())

    def _resolve_pattern(self, p: Optional[str]) -> Optional[str]:
        if p is None:
            return None
        pp = Path(os.path.expandvars(os.path.expanduser(p)))
        if pp.is_absolute():
            return str(pp)
        return str((self.base_dir / pp))

    def _ensure_list(self, v: Any) -> list:
        if v is None:
            return []
        if isinstance(v, list):
            return v
        return [v]

    def _resolve_env_value(self, spec: Any) -> Optional[str]:
        if spec is None:
            return None
        if isinstance(spec, str):
            return os.path.expandvars(spec)
        if isinstance(spec, dict):
            if "value" in spec:
                return str(spec["value"]) if spec["value"] is not None else None
            env_name = spec.get("from_env")
            default = spec.get("default")
            required = bool(spec.get("required", False))
            val = None
            if env_name:
                val = os.environ.get(env_name, None)
            if val is None:
                val = default
            if required and (val is None or val == ""):
                raise ValueError(
                    f"Required environment variable '{env_name}' is not set and no default provided")
            return None if val is None else str(val)
        # Fallback: cast to string
        return str(spec)

    def _normalize_command(self, cfg: Dict[str, Any]) -> Dict[str, Any]:
        program = cfg.get("program")
        command = cfg.get("command")

        args = cfg.get("args", [])
        if command and program:
            # If both provided, prefer explicit program/args
            command = None

        if command:
            if isinstance(command, str):
                parts = shlex.split(command)
            elif isinstance(command, list):
                parts = [str(x) for x in command]
            else:
                raise TypeError("command must be a string or list")
            if not parts:
                raise ValueError("command must not be empty")
            program = parts[0]
            args = parts[1:] + self._ensure_list(args)
        else:
            if not program:
                raise ValueError(
                    "Either 'program' or 'command' must be provided under command configuration")
            if not isinstance(program, str):
                raise TypeError("'program' must be a string")
            args = [str(a) for a in self._ensure_list(args)]

        env_spec = cfg.get("env", {}) or {}
        if not isinstance(env_spec, dict):
            raise TypeError("env must be a mapping/dict if provided")

        env: Dict[str, str] = {}
        for k, v in env_spec.items():
            resolved = self._resolve_env_value(v)
            if resolved is not None:
                env[str(k)] = resolved

        cwd = cfg.get("cwd")
        cwd_resolved = self._resolve_path(cwd) if cwd else None

        return {
            "program": str(program),
            "args": args,
            "env": env,
            "cwd": cwd_resolved,
        }

    def _normalize_files(self, files_cfg: Dict[str, Any]) -> Dict[str, Any]:
        files_cfg = files_cfg or {}
        roots = [self._resolve_path(
            p) for p in self._ensure_list(files_cfg.get("roots"))]
        allowed = [self._resolve_pattern(p) for p in self._ensure_list(
            files_cfg.get("allow") or files_cfg.get("allowed"))]
        blocked = [self._resolve_pattern(p) for p in self._ensure_list(
            files_cfg.get("deny") or files_cfg.get("blocked"))]

        # Filter out None entries
        roots = [p for p in roots if p]
        allowed = [p for p in allowed if p]
        blocked = [p for p in blocked if p]

        return {
            "roots": roots,
            "allowed": allowed,
            "blocked": blocked,
        }

    def _normalize_logging(self, log_cfg: Dict[str, Any]) -> Dict[str, Any]:
        log_cfg = log_cfg or {}
        level = (log_cfg.get("level") or "INFO").upper()
        file_path = log_cfg.get("file") or log_cfg.get("path")
        resolved_file = self._resolve_path(file_path) if file_path else None
        fmt = log_cfg.get(
            "format") or "%(asctime)s %(levelname)s %(name)s %(message)s"
        rotation = log_cfg.get("rotate") or log_cfg.get("rotation") or {}

        return {
            "level": level,
            "file": resolved_file,
            "format": fmt,
            "rotation": {
                "when": rotation.get("when", "midnight"),
                "interval": int(rotation.get("interval", 1)),
                "backup_count": int(rotation.get("backup_count", rotation.get("backupCount", 7))),
                "max_bytes": int(rotation.get("max_bytes", rotation.get("maxBytes", 0))),
            },
        }

    def _normalize_timeouts(self, timeouts: Dict[str, Any]) -> Dict[str, Any]:
        timeouts = timeouts or {}
        return {
            "start": float(timeouts.get("start", 30.0)),
            "request": float(timeouts.get("request", 120.0)),
            "shutdown": float(timeouts.get("shutdown", 10.0)),
        }

    def _normalize_retries(self, retries: Dict[str, Any]) -> Dict[str, Any]:
        retries = retries or {}
        return {
            "start": int(retries.get("start", 3)),
            "request": int(retries.get("request", 0)),
            "backoff": float(retries.get("backoff", 2.0)),
            "max_backoff": float(retries.get("max_backoff", 30.0)),
            "jitter": float(retries.get("jitter", 0.1)),
        }

    def generate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Generate a full MCP server configuration from a simplified config.
        Args:
            config: Simplified configuration dictionary
        Returns:
            Complete MCP server configuration
        '''
        if not isinstance(config, dict):
            raise TypeError("config must be a dictionary")

        name = config.get("name")
        if not name or not isinstance(name, str):
            raise ValueError("config['name'] must be a non-empty string")

        transport = config.get("transport") or {}
        if isinstance(transport, str):
            transport = {"type": transport}
        transport_type = transport.get("type", "stdio")
        transport_cfg = {"type": transport_type}
        # Allow passing through extra transport-specific fields
        for k, v in transport.items():
            if k != "type":
                transport_cfg[k] = v

        command_cfg = self._normalize_command(config.get("command", config))
        files_cfg = self._normalize_files(config.get("files", {}))
        logging_cfg = self._normalize_logging(config.get("logging", {}))
        timeouts_cfg = self._normalize_timeouts(config.get("timeouts", {}))
        retries_cfg = self._normalize_retries(config.get("retries", {}))

        capabilities = config.get("capabilities", {})
        if not isinstance(capabilities, dict):
            raise TypeError("capabilities must be a dictionary if provided")

        result: Dict[str, Any] = {
            "mcp": {
                "name": name,
                "version": str(config.get("version", "1.0")),
                "transport": transport_cfg,
                "command": command_cfg,
                "files": files_cfg,
                "logging": logging_cfg,
                "timeouts": timeouts_cfg,
                "retries": retries_cfg,
                "capabilities": capabilities,
            }
        }

        extras = config.get("extra") or {}
        if extras and isinstance(extras, dict):
            # Merge extra top-level fields under "mcp"
            result["mcp"].update(
                {k: v for k, v in extras.items() if k not in result["mcp"]})

        return result

    def write_config(self, config: Dict[str, Any], output_path: str) -> None:
        '''
        Write the generated configuration to a file.
        Args:
            config: The simplified configuration dictionary
            output_path: Path to write the generated configuration
        '''
        full_cfg = self.generate_config(config)
        out_path = Path(output_path).expanduser()
        if not out_path.is_absolute():
            out_path = (self.base_dir / out_path).resolve()

        out_path.parent.mkdir(parents=True, exist_ok=True)
        suffix = out_path.suffix.lower()

        if suffix in (".json", ""):
            with out_path.with_suffix(".json") if suffix == "" else out_path as fpath:
                with open(fpath, "w", encoding="utf-8") as f:
                    json.dump(full_cfg, f, indent=2, sort_keys=True)
            return

        if suffix in (".yaml", ".yml"):
            try:
                import yaml  # type: ignore
            except Exception as e:
                raise RuntimeError(
                    "PyYAML is required to write YAML configuration") from e
            with open(out_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(full_cfg, f, sort_keys=False)
            return

        if suffix == ".toml":
            try:
                try:
                    import tomli_w as toml_writer  # type: ignore
                    dumps = toml_writer.dumps
                except Exception:
                    import toml  # type: ignore
                    dumps = toml.dumps  # type: ignore
            except Exception as e:
                raise RuntimeError(
                    "A TOML writer (tomli-w or toml) is required to write TOML configuration") from e
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(dumps(full_cfg))
            return

        raise ValueError(f"Unsupported output file format: {suffix}")
