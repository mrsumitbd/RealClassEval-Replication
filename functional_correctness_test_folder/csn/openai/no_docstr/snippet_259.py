
import json
import os
from typing import Any, Dict, Optional, Union

# Optional YAML support – fall back to JSON if unavailable
try:
    import yaml  # type: ignore
    _YAML_AVAILABLE = True
except Exception:
    _YAML_AVAILABLE = False


class WCxf:
    """
    Minimal implementation of a WCxf (Weakly Coupled Effective Field Theory) container.
    It can load from and dump to JSON or YAML streams.
    """

    def __init__(self, data: Optional[Dict[str, Any]] = None):
        self._data: Dict[str, Any] = data or {}

    @classmethod
    def load(
        cls,
        stream: Union[str, os.PathLike, Any],
        fmt: str = "json",
        **kwargs: Any,
    ) -> "WCxf":
        """
        Load a WCxf instance from a stream or file path.

        Parameters
        ----------
        stream : str | PathLike | file-like
            If a string or PathLike, it is treated as a file path.
            Otherwise, it must have a ``read`` method returning a string.
        fmt : str, optional
            Format of the input. Supported: 'json', 'yaml'.
            Default is 'json'.
        **kwargs
            Additional keyword arguments passed to the underlying parser.

        Returns
        -------
        WCxf
            A new instance populated with the parsed data.
        """
        # Resolve the actual content string
        if isinstance(stream, (str, os.PathLike)):
            if not os.path.exists(stream):
                raise FileNotFoundError(f"File not found: {stream}")
            with open(stream, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            # Assume file-like object
            try:
                content = stream.read()
            except AttributeError as exc:
                raise TypeError(
                    "stream must be a file path or a file-like object with a read() method"
                ) from exc

        # Parse according to format
        fmt = fmt.lower()
        if fmt == "json":
            data = json.loads(content, **kwargs)
        elif fmt in ("yaml", "yml"):
            if not _YAML_AVAILABLE:
                raise RuntimeError(
                    "YAML support requires PyYAML to be installed."
                )
            data = yaml.safe_load(content)
        else:
            raise ValueError(f"Unsupported format: {fmt!r}")

        if not isinstance(data, dict):
            raise ValueError("Parsed data must be a dictionary")

        return cls(data)

    def dump(
        self,
        stream: Optional[Union[str, os.PathLike, Any]] = None,
        fmt: str = "json",
        **kwargs: Any,
    ) -> Optional[str]:
        """
        Dump the WCxf instance to a stream or return a string.

        Parameters
        ----------
        stream : str | PathLike | file-like | None, optional
            If provided, the output is written to this stream or file path.
            If None, the serialized string is returned.
        fmt : str, optional
            Output format: 'json' or 'yaml'. Default is 'json'.
        **kwargs
            Additional keyword arguments passed to the serializer.

        Returns
        -------
        str | None
            The serialized string if stream is None; otherwise None.
        """
        fmt = fmt.lower()
        if fmt == "json":
            serialized = json.dumps(
                self._data,
                indent=kwargs.pop("indent", 4),
                sort_keys=kwargs.pop("sort_keys", True),
                **kwargs,
            )
        elif fmt in ("yaml", "yml"):
            if not _YAML_AVAILABLE:
                raise RuntimeError(
                    "YAML support requires PyYAML to be installed."
                )
            # yaml.safe_dump expects a dict; ensure we pass the data
            serialized = yaml.safe_dump(
                self._data,
                default_flow_style=False,
                sort_keys=kwargs.pop("sort_keys", True),
                **kwargs,
            )
        else:
            raise ValueError(f"Unsupported format: {fmt!r}")

        if stream is None:
            return serialized

        # Write to the provided stream
        if isinstance(stream, (str, os.PathLike)):
            with open(stream, "w", encoding="utf-8") as f:
                f.write(serialized)
        else:
            try:
                stream.write(serialized)
            except AttributeError as exc:
                raise TypeError(
                    "stream must be a file path or a file-like object with a write() method"
                ) from exc

        return None

    # Convenience methods for attribute access
    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._data!r})"
