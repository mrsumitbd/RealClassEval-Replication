import sys
import os
from collections.abc import Mapping


class _AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.update(*args, **kwargs)

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError as e:
            raise AttributeError(item) from e

    def __setattr__(self, key, value):
        if key.startswith('_'):
            return super().__setattr__(key, value)
        self[key] = value

    def __delattr__(self, item):
        try:
            del self[item]
        except KeyError as e:
            raise AttributeError(item) from e

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = self._wrap(v)

    def __setitem__(self, key, value):
        super().__setitem__(key, self._wrap(value))

    @classmethod
    def _wrap(cls, value):
        if isinstance(value, Mapping):
            return _AttrDict(value)
        return value


class _SafeFormatDict(dict):
    def __missing__(self, key):
        return ''


class Template:

    def __init__(self):
        pass

    def _to_iter(self, sources):
        if sources is None:
            return []
        if isinstance(sources, (str, os.PathLike)) or hasattr(sources, 'read'):
            return [sources]
        try:
            iter(sources)
        except TypeError:
            return [sources]
        return list(sources)

    def _read_source(self, src):
        if hasattr(src, 'read'):
            return src.read()
        if isinstance(src, (str, os.PathLike)):
            p = os.fspath(src)
            if os.path.exists(p) and os.path.isfile(p):
                with open(p, 'r', encoding='utf-8') as f:
                    return f.read()
            return str(src)
        return str(src)

    def render(self, sources, config, out=sys.stdout):
        cfg = config or {}
        wrapped = _AttrDict(cfg)
        fmt_map = _SafeFormatDict(wrapped)
        rendered_parts = []
        for src in self._to_iter(sources):
            text = self._read_source(src)
            rendered = text.format_map(fmt_map)
            rendered_parts.append(rendered)
        output = ''.join(rendered_parts)
        if out is not None:
            out.write(output)
        return output
