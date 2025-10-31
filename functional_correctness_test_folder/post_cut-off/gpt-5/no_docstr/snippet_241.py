from __future__ import annotations

import configparser
import json
import os
from pathlib import Path
from typing import Any


class Configuration:
    def __init__(self) -> None:
        self._config: dict[str, Any] = {}
        self.load_env()
        config_file = os.getenv("CONFIG_FILE")
        if config_file:
            self._config = self.load_config(config_file)

    @staticmethod
    def load_env() -> None:
        try:
            from dotenv import load_dotenv  # type: ignore
        except Exception:
            return
        load_dotenv(override=False)

    @staticmethod
    def load_config(file_path: str) -> dict[str, Any]:
        path = Path(file_path).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        suffix = path.suffix.lower()

        if suffix == ".json":
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("Top-level JSON must be an object")
            return data

        if suffix in {".toml"}:
            try:
                import tomllib  # Python 3.11+
            except Exception as e:
                raise ImportError(
                    "Reading TOML requires Python 3.11+ (tomllib).") from e
            with path.open("rb") as f:
                data = tomllib.load(f)
            if not isinstance(data, dict):
                raise ValueError("Top-level TOML must be a table")
            return data  # type: ignore[return-value]

        if suffix in {".yaml", ".yml"}:
            try:
                import yaml  # type: ignore
            except Exception as e:
                raise ImportError(
                    "Reading YAML requires PyYAML installed.") from e
            with path.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)  # type: ignore
            if data is None:
                return {}
            if not isinstance(data, dict):
                raise ValueError("Top-level YAML must be a mapping")
            return data  # type: ignore[return-value]

        if suffix in {".ini", ".cfg"}:
            parser = configparser.ConfigParser()
            with path.open("r", encoding="utf-8") as f:
                parser.read_file(f)
            result: dict[str, Any] = {
                s: dict(parser.items(s)) for s in parser.sections()}
            if parser.defaults():
                result["DEFAULT"] = dict(parser.defaults())
            return result

        if suffix == ".env":
            result: dict[str, Any] = {}
            with path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        continue
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    result[key] = value
            return result

        raise ValueError(f"Unsupported configuration file type: {suffix}")

    @property
    def llm_api_key(self) -> str:
        env_keys = [
            "LLM_API_KEY",
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "AZURE_OPENAI_API_KEY",
            "GEMINI_API_KEY",
        ]
        for k in env_keys:
            val = os.getenv(k)
            if val:
                return val

        cfg_keys = [
            "llm_api_key",
            "openai_api_key",
            "anthropic_api_key",
            "azure_openai_api_key",
            "gemini_api_key",
        ]
        for k in cfg_keys:
            v = self._config.get(k)
            if isinstance(v, str) and v:
                return v

        raise KeyError(
            "No LLM API key found in environment variables or configuration."
        )
