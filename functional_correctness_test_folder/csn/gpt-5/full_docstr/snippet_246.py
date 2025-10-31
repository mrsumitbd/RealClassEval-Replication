from pathlib import Path
from collections.abc import Mapping


class Config:
    '''Provide tool to managed config
    '''

    _SOURCE_KEYS = ("source", "src", "source_file", "sourceFile")
    _TEMPLATE_KEYS = ("template", "template_path",
                      "templateFile", "template_file")

    def validate(self, config):
        '''Validate that the source file is ok
        '''
        cfg = self._ensure_mapping_like(config)
        value = self._get_any(cfg, self._SOURCE_KEYS)
        if value is None:
            raise KeyError(
                f"Missing source key. Expected one of: {', '.join(self._SOURCE_KEYS)}")

        path = self._coerce_path(value)
        if not path.exists():
            raise FileNotFoundError(f"Source file not found: {path}")
        if not path.is_file():
            raise IsADirectoryError(f"Source path is not a file: {path}")
        return True

    def get_template_from_config(self, config):
        '''Retrieve a template path from the config object
        '''
        cfg = self._ensure_mapping_like(config)
        value = self._get_any(cfg, self._TEMPLATE_KEYS)
        if value is None:
            raise KeyError(
                f"Missing template key. Expected one of: {', '.join(self._TEMPLATE_KEYS)}")

        path = self._coerce_path(value)
        if not path.exists():
            raise FileNotFoundError(f"Template file not found: {path}")
        if not path.is_file():
            raise IsADirectoryError(f"Template path is not a file: {path}")
        return str(path)

    def _ensure_mapping_like(self, config):
        if isinstance(config, Mapping):
            return config
        # Allow simple objects with attributes

        class AttrMapping(dict):
            def __init__(self, obj):
                super().__init__()
                for k in dir(obj):
                    if k.startswith("_"):
                        continue
                    try:
                        v = getattr(obj, k)
                    except Exception:
                        continue
                    if not callable(v):
                        self[k] = v
        try:
            return AttrMapping(config)
        except Exception as e:
            raise TypeError(
                "Config must be a mapping or an object with attributes.") from e

    def _get_any(self, cfg, keys):
        for k in keys:
            if k in cfg and cfg[k] not in (None, ""):
                return cfg[k]
        return None

    def _coerce_path(self, value):
        if isinstance(value, Path):
            return value.expanduser().resolve(strict=False)
        if isinstance(value, (str, bytes)):
            return Path(value).expanduser().resolve(strict=False)
        raise TypeError(
            f"Path value must be str, bytes, or Path, got {type(value).__name__}")
