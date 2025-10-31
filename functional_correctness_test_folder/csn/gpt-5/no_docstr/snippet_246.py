from pathlib import Path
from typing import Any, Mapping, Optional


class Config:
    def validate(self, config: Any) -> dict:
        if not isinstance(config, Mapping):
            raise TypeError("config must be a mapping/dict")
        has_template = "template" in config
        has_path = "template_path" in config

        if not has_template and not has_path:
            raise ValueError(
                "config must contain either 'template' or 'template_path'")
        if has_template and has_path:
            raise ValueError(
                "config must not contain both 'template' and 'template_path'")

        normalized: dict = {}

        if has_template:
            template = config["template"]
            if not isinstance(template, str):
                raise TypeError("'template' must be a string")
            normalized["source"] = "inline"
            normalized["template"] = template

        if has_path:
            path_val = config["template_path"]
            if isinstance(path_val, (str, Path)):
                path = Path(path_val)
            else:
                raise TypeError(
                    "'template_path' must be a str or pathlib.Path")
            if not path.exists():
                raise ValueError(f"template file does not exist: {path}")
            if not path.is_file():
                raise ValueError(f"template path is not a file: {path}")
            normalized["source"] = "file"
            normalized["template_path"] = path

        encoding = config.get("encoding", "utf-8")
        if not isinstance(encoding, str):
            raise TypeError("'encoding' must be a string")
        normalized["encoding"] = encoding

        return normalized

    def get_template_from_config(self, config: Any) -> str:
        cfg = self.validate(config)
        if cfg["source"] == "inline":
            return cfg["template"]
        try:
            return Path(cfg["template_path"]).read_text(encoding=cfg["encoding"])
        except OSError as e:
            raise ValueError(f"failed to read template file: {e}") from e
