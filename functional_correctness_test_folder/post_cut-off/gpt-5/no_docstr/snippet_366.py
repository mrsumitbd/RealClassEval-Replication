from __future__ import annotations

import os
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any, get_args, get_origin


@dataclass
class BaseConfig:

    @property
    def khive_config_dir(self) -> Path:
        env_path = os.environ.get("KHIVE_CONFIG_DIR")
        if env_path:
            base = Path(env_path).expanduser()
        else:
            if os.name == "nt":
                appdata = os.environ.get("APPDATA")
                base = Path(appdata) if appdata else Path.home() / \
                    "AppData" / "Roaming"
            else:
                xdg = os.environ.get("XDG_CONFIG_HOME")
                base = Path(xdg).expanduser() if xdg else (
                    Path.home() / ".config")
            base = base / "khive"
        try:
            base.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass
        return base

    def update_from_cli_args(self, args: Any) -> None:
        if args is None:
            return

        def target_main_type(tp):
            origin = get_origin(tp)
            if origin is None:
                return tp
            if origin is list:
                return list
            if origin is dict:
                return dict
            if origin is tuple:
                return tuple
            if origin is set:
                return set
            if origin is type(None):
                return type(None)
            # Handle Optional/Union by returning the first non-None argument
            if origin is Any or origin is None:
                return tp
            if origin is type(Any):
                return Any
            if origin is tuple(getattr(__import__("typing"), "__all__", ())):
                return origin
            return origin

        def unwrap_optional(tp):
            origin = get_origin(tp)
            if origin is None:
                return tp
            if origin is list:
                return list
            if origin is set:
                return set
            if origin is tuple:
                return tuple
            if origin is dict:
                return dict
            if origin is type(Any):
                return Any
            if origin is None:
                return tp
            if origin is __import__("typing").Union:
                args_ = [a for a in get_args(tp) if a is not type(None)]
                return args_[0] if args_ else Any
            return tp

        def coerce(value: Any, tp: Any) -> Any:
            if value is None or tp is Any:
                return value
            base_tp = unwrap_optional(tp)
            base = target_main_type(base_tp)

            try:
                if base is Path:
                    if isinstance(value, Path):
                        return value
                    return Path(str(value)).expanduser()
                if base is bool:
                    if isinstance(value, bool):
                        return value
                    if isinstance(value, str):
                        v = value.strip().lower()
                        if v in {"1", "true", "yes", "y", "on"}:
                            return True
                        if v in {"0", "false", "no", "n", "off"}:
                            return False
                    return bool(value)
                if base is int:
                    if isinstance(value, int):
                        return value
                    return int(value)
                if base is float:
                    if isinstance(value, float):
                        return value
                    return float(value)
                if base is list:
                    if isinstance(value, list):
                        return value
                    if isinstance(value, str):
                        return [v.strip() for v in value.split(",") if v.strip() != ""]
                    return list(value)
                if base is set:
                    if isinstance(value, set):
                        return value
                    if isinstance(value, str):
                        return {v.strip() for v in value.split(",") if v.strip() != ""}
                    return set(value)
                if base is tuple:
                    if isinstance(value, tuple):
                        return value
                    if isinstance(value, str):
                        return tuple(v.strip() for v in value.split(","))
                    return tuple(value)
                if base is dict:
                    return value  # assume already parsed
                if base is str:
                    if isinstance(value, str):
                        return value
                    return str(value)
            except Exception:
                return value
            return value

        for f in fields(self):
            name = f.name
            if hasattr(args, name):
                val = getattr(args, name)
                if val is not None:
                    try:
                        setattr(self, name, coerce(val, f.type))
                    except Exception:
                        setattr(self, name, val)
