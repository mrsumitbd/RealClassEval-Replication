from pathlib import Path
from typing import Optional, Dict, Any, TYPE_CHECKING
import json
from json import JSONDecodeError

if TYPE_CHECKING:
    from .settings import Settings  # type: ignore[unused-ignore]


class LastUsedParams:
    """Manages last used parameters persistence (moved from last_used.py)."""

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        """Initialize with config directory."""
        self.config_dir: Path = config_dir if config_dir is not None else (
            Path.home() / ".config")
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self._file: Path = self.config_dir / "last_used.json"

    def save(self, settings: "Settings") -> None:
        """Save current settings as last used."""
        def to_dict(obj: Any) -> Dict[str, Any]:
            if isinstance(obj, dict):
                return obj
            if hasattr(obj, "to_dict") and callable(getattr(obj, "to_dict")):
                return obj.to_dict()  # type: ignore[no-any-return]
            if hasattr(obj, "dict") and callable(getattr(obj, "dict")):
                return obj.dict()  # type: ignore[no-any-return]
            if hasattr(obj, "__dict__"):
                return {k: v for k, v in vars(obj).items() if not k.startswith("_")}
            raise TypeError("Unsupported settings object for serialization")

        data: Dict[str, Any] = to_dict(settings)
        tmp_path = self._file.with_suffix(self._file.suffix + ".tmp")
        self.config_dir.mkdir(parents=True, exist_ok=True)
        try:
            with tmp_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2,
                          default=lambda o: getattr(o, "__dict__", str(o)))
            tmp_path.replace(self._file)
        finally:
            if tmp_path.exists():
                try:
                    tmp_path.unlink()
                except Exception:
                    pass

    def load(self) -> Dict[str, Any]:
        """Load last used parameters."""
        if not self._file.exists():
            return {}
        try:
            with self._file.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
            return {}
        except (OSError, JSONDecodeError):
            return {}

    def clear(self) -> None:
        """Clear last used parameters."""
        try:
            if self._file.exists():
                self._file.unlink()
        except Exception:
            pass

    def exists(self) -> bool:
        """Check if last used params exist."""
        return self._file.is_file()
