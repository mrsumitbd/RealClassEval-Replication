class WCxf:
    def __init__(self, data=None):
        self.data = data if data is not None else {}

    @classmethod
    def load(cls, stream, fmt=None, **kwargs):
        import json

        yaml = None
        try:
            import yaml as _yaml  # optional
            yaml = _yaml
        except Exception:
            pass

        def _is_file_like(obj):
            return hasattr(obj, 'read') and callable(obj.read)

        def _read_from_stream(s):
            if _is_file_like(s):
                return s.read()
            if isinstance(s, (bytes, bytearray)):
                return s.decode(kwargs.get('encoding', 'utf-8'))
            if isinstance(s, str):
                # If it's a path, read file
                try:
                    with open(s, 'r', encoding=kwargs.get('encoding', 'utf-8')) as f:
                        return f.read()
                except (OSError, IOError):
                    # Not a path or unreadable; treat as raw content
                    return s
            if isinstance(s, dict):
                return s  # already data
            raise TypeError("Unsupported stream type for load")

        def _infer_fmt(s, given_fmt):
            if given_fmt:
                return given_fmt.lower()
            # infer from filename if applicable
            if isinstance(stream, str):
                lower = stream.lower()
                if lower.endswith('.json'):
                    return 'json'
                if lower.endswith('.yml') or lower.endswith('.yaml'):
                    return 'yaml'
            # try content sniffing
            txt = s if isinstance(s, str) else None
            if isinstance(s, dict):
                return 'json'
            if txt is not None:
                t = txt.lstrip()
                if t.startswith('{') or t.startswith('['):
                    return 'json'
                # fallback to yaml if available
                if yaml is not None:
                    return 'yaml'
            return 'json'

        # Fast path if dict provided
        if isinstance(stream, dict):
            return cls(stream.copy())

        content = _read_from_stream(stream)
        fmt_final = _infer_fmt(content, fmt)

        if fmt_final == 'json':
            if isinstance(content, dict):
                data = content
            else:
                data = json.loads(content, **{k: v for k, v in kwargs.items() if k in {
                                  'cls', 'parse_float', 'parse_int', 'parse_constant', 'object_hook', 'object_pairs_hook'}})
            return cls(data)
        elif fmt_final == 'yaml':
            if yaml is None:
                raise ValueError(
                    "YAML support requires PyYAML to be installed")
            if isinstance(content, dict):
                data = content
            else:
                data = yaml.safe_load(content)
            return cls(data)
        else:
            raise ValueError(f"Unsupported format: {fmt_final}")

    def dump(self, stream=None, fmt='json', **kwargs):
        import json

        yaml = None
        try:
            import yaml as _yaml  # optional
            yaml = _yaml
        except Exception:
            pass

        fmt = (fmt or 'json').lower()

        def _is_file_like(obj):
            return hasattr(obj, 'write') and callable(obj.write)

        def _serialize(data):
            if fmt == 'json':
                if stream is None:
                    return json.dumps(data, **{**{'ensure_ascii': False, 'indent': 2}, **kwargs})
                else:
                    return json.dumps(data, **kwargs)
            elif fmt == 'yaml':
                if yaml is None:
                    raise ValueError(
                        "YAML support requires PyYAML to be installed")
                default_opts = {'sort_keys': False}
                opts = {**default_opts, **kwargs}
                return yaml.safe_dump(data, **opts)
            else:
                raise ValueError(f"Unsupported format: {fmt}")

        if stream is None:
            return _serialize(self.data)

        if _is_file_like(stream):
            text = _serialize(self.data)
            stream.write(text)
            return None

        if isinstance(stream, (str, bytes, bytearray)):
            path = stream.decode() if isinstance(stream, (bytes, bytearray)) else stream
            encoding = kwargs.pop('encoding', 'utf-8')
            text = _serialize(self.data)
            with open(path, 'w', encoding=encoding) as f:
                f.write(text)
            return None

        raise TypeError("Unsupported stream type for dump")
