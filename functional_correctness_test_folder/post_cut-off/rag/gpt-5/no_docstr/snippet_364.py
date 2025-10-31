from dataclasses import dataclass, asdict, is_dataclass
from typing import Any, Optional


@dataclass
class CLIResult:
    """Standard result structure for CLI commands."""
    success: bool
    message: str = ""
    data: Any = None
    error: Optional[str] = None
    code: Optional[int] = None

    def is_success(self) -> bool:
        """Check if the result represents success."""
        return self.success

    def to_dict(self) -> dict[str, Any]:
        """Convert result to dictionary for JSON output."""
        def _serialize(value: Any) -> Any:
            if value is None:
                return None
            if is_dataclass(value):
                return asdict(value)
            if hasattr(value, "to_dict") and callable(getattr(value, "to_dict")):
                try:
                    return value.to_dict()
                except Exception:
                    pass
            if isinstance(value, dict):
                return {k: _serialize(v) for k, v in value.items()}
            if isinstance(value, (list, tuple, set)):
                return [_serialize(v) for v in value]
            return value

        result: dict[str, Any] = {"success": self.success}
        if self.message:
            result["message"] = self.message
        if self.code is not None:
            result["code"] = self.code
        if self.error is not None:
            result["error"] = self.error
        if self.data is not None:
            result["data"] = _serialize(self.data)
        return result
