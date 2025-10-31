
import json
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


class WCxf:
    """Base class for WCxf files (not meant to be used directly)."""

    def __init__(self, **data):
        """Store the data dictionary."""
        self._data = data

    @property
    def data(self):
        """Return the underlying data dictionary."""
        return self._data

    @classmethod
    def load(cls, stream, **kwargs):
        """
        Load the object data from a JSON or YAML file.

        Parameters
        ----------
        stream : file-like object or str
            If a string, it is treated as a file path.
        **kwargs
            Additional keyword arguments are passed to
            :func:`json.load` or :func:`yaml.safe_load`.

        Returns
        -------
        WCxf
            An instance of the class with the loaded data.
        """
        # Resolve stream to a file object
        if isinstance(stream, str):
            f = open(stream, "r", encoding=kwargs.pop("encoding", "utf-8"))
            close_f = True
        else:
            f = stream
            close_f = False

        try:
            fmt = kwargs.pop("fmt", None)
            if fmt is None:
                # Guess format from file extension if possible
                if hasattr(stream, "name") and stream.name.endswith((".yaml", ".yml")):
                    fmt = "yaml"
                else:
                    fmt = "json"

            if fmt == "json":
                data = json.load(f, **kwargs)
            elif fmt == "yaml":
                if yaml is None:  # pragma: no cover
                    raise ImportError("PyYAML is required for YAML support")
                data = yaml.safe_load(f, **kwargs)
            else:
                raise ValueError(f"Unsupported format: {fmt!r}")
        finally:
            if close_f:
                f.close()

        return cls(**data)

    def dump(self, stream=None, fmt="json", **kwargs):
        """
        Dump the object data to a JSON or YAML file.

        Parameters
        ----------
        stream : file-like object or None
            If None (default), return a string. Otherwise, write to the
            provided writable file-like object.
        fmt : str
            Format, should be 'json' (default) or 'yaml'.
        **kwargs
            Additional keyword arguments are passed to
            :func:`json.dump`/`json.dumps` or :func:`yaml.safe_dump`.

        Returns
        -------
        str or None
            If ``stream`` is None, returns the serialized string.
            Otherwise, returns None.
        """
        data = self._data

        if fmt == "json":
            if stream is None:
                return json.dumps(data, **kwargs)
            else:
                json.dump(data, stream, **kwargs)
                return None
        elif fmt == "yaml":
            if yaml is None:  # pragma: no cover
                raise ImportError("PyYAML is required for YAML support")
            if stream is None:
                return yaml.safe_dump(data, **kwargs)
            else:
                yaml.safe_dump(data, stream, **kwargs)
                return None
        else:
            raise ValueError(f"Unsupported format: {fmt!r}")
