import uuid
from typing import Any

class RequestContext:
    """
    Request-scoped context object that holds trace_id and other request data.

    This provides a Flask g-like object for FastAPI applications.
    """

    def __init__(self, trace_id: str | None=None):
        self.trace_id = trace_id or str(uuid.uuid4())
        self._data: dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        """Set a value in the context."""
        self._data[key] = value

    def get(self, key: str, default: Any | None=None) -> Any:
        """Get a value from the context."""
        return self._data.get(key, default)

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith('_') or name == 'trace_id':
            super().__setattr__(name, value)
        elif not hasattr(self, '_data'):
            super().__setattr__(name, value)
        else:
            self._data[name] = value

    def __getattr__(self, name: str) -> Any:
        if hasattr(self, '_data') and name in self._data:
            return self._data[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def to_dict(self) -> dict[str, Any]:
        """Convert context to dictionary."""
        return {'trace_id': self.trace_id, 'data': self._data.copy()}