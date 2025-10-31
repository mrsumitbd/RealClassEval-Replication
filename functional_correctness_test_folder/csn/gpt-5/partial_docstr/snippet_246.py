from pathlib import Path
from typing import Any, Optional


class Config:
    '''Provide tool to managed config
    '''

    def validate(self, config: Any) -> bool:
        if config is None:
            raise ValueError("config cannot be None")

        template = self.get_template_from_config(config)
        if template is None:
            raise ValueError("config does not contain a template path")

        if not isinstance(template, (str, Path)):
            raise TypeError("template must be a string or a pathlib.Path")

        template_str = str(template).strip()
        if not template_str:
            raise ValueError("template path cannot be empty")

        return True

    def get_template_from_config(self, config: Any) -> Optional[str]:
        '''Retrieve a template path from the config object
        '''
        # Direct path-like inputs
        if isinstance(config, (str, Path)):
            s = str(config).strip()
            return s if s else None

        # Mapping-like (dict) inputs
        if isinstance(config, dict):
            candidates = (
                config.get("template"),
                config.get("template_path"),
                config.get("template_file"),
                config.get("template_name"),
            )
            for cand in candidates:
                if isinstance(cand, (str, Path)) and str(cand).strip():
                    return str(cand)

            # Nested under common namespaces
            paths = config.get("paths") or config.get("path") or {}
            if isinstance(paths, dict):
                cand = paths.get("template") or paths.get(
                    "template_path") or paths.get("template_file")
                if isinstance(cand, (str, Path)) and str(cand).strip():
                    return str(cand)

            return None

        # Object with attributes
        for attr in ("template", "template_path", "template_file", "template_name"):
            if hasattr(config, attr):
                cand = getattr(config, attr)
                if isinstance(cand, (str, Path)) and str(cand).strip():
                    return str(cand)

        return None
