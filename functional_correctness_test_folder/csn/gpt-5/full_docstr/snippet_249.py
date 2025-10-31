import sys
import os
from pathlib import Path
from collections.abc import Mapping, Iterable

try:
    import jinja2 as _jinja2  # Optional
except Exception:  # pragma: no cover
    _jinja2 = None


class Template:
    '''Provide tool to managed templates
    '''

    def __init__(self):
        '''Class instantiation
        '''
        self.default_engine = 'auto'  # 'auto' | 'format' | 'jinja2'

    def render(self, sources, config, out=sys.stdout):
        '''Render the documentation as defined in config Object
        '''
        cfg = self._normalize_config(config)
        template = self._load_template(cfg)
        context = self._build_context(sources, cfg)

        engine = cfg.get('engine', self.default_engine)
        if engine == 'auto':
            engine = self._detect_engine(template)

        if engine == 'jinja2':
            if _jinja2 is None:
                raise RuntimeError("Jinja2 engine requested but not available")
            rendered = self._render_jinja2(template, context, cfg)
        elif engine == 'format':
            rendered = self._render_format(template, context)
        else:
            raise ValueError(f"Unsupported engine: {engine}")

        if out is None:
            return rendered

        self._write_output(rendered, out, cfg)
        return rendered

    # Helpers

    def _normalize_config(self, config):
        if config is None:
            return {}
        if isinstance(config, Mapping):
            cfg = dict(config)
        else:
            # Fallback to attribute-based object
            cfg = {k: getattr(config, k)
                   for k in dir(config) if not k.startswith('_')}
        return cfg

    def _load_template(self, cfg):
        tpl = cfg.get('template')
        if tpl is None:
            raise ValueError("config must include 'template' (string or path)")

        # If template is a path and exists, read it
        if isinstance(tpl, (str, os.PathLike)):
            p = Path(tpl)
            if p.exists() and p.is_file():
                return p.read_text(encoding=cfg.get('encoding', 'utf-8'))
        # Else treat as inline template string
        if not isinstance(tpl, str):
            raise TypeError(
                "template must be a string or a path to a template file")
        return tpl

    def _build_context(self, sources, cfg):
        ctx = {}
        extra = cfg.get('context') or {}
        if not isinstance(extra, Mapping):
            raise TypeError("config['context'] must be a mapping if provided")
        ctx.update(extra)

        # Normalize sources
        normalized = self._normalize_sources(sources, cfg)
        # Provide both flat and namespaced access
        ctx.setdefault('sources', normalized)
        # If mapping and values are scalar/text, flatten top-level keys, without overwriting explicit context
        if isinstance(normalized, Mapping):
            for k, v in normalized.items():
                if k not in ctx:
                    ctx[k] = v
        return ctx

    def _normalize_sources(self, sources, cfg):
        # Accept:
        # - Mapping[str, Any]
        # - path string/Path -> read text
        # - Iterable of paths -> dict name->text
        # - file-like -> read
        encoding = cfg.get('source_encoding', cfg.get('encoding', 'utf-8'))

        # File-like
        if hasattr(sources, 'read'):
            return sources.read()

        # Single path
        if isinstance(sources, (str, os.PathLike)):
            p = Path(sources)
            if p.exists():
                if p.is_file():
                    return p.read_text(encoding=encoding)
                if p.is_dir():
                    return self._read_dir(p, encoding)
            # Not an existing path: return as-is string
            return str(sources)

        # Mapping
        if isinstance(sources, Mapping):
            return {str(k): self._maybe_read(v, encoding) for k, v in sources.items()}

        # Iterable of paths/values
        if isinstance(sources, Iterable):
            result = {}
            for item in sources:
                if isinstance(item, (str, os.PathLike)):
                    p = Path(item)
                    if p.exists() and p.is_file():
                        result[p.stem] = p.read_text(encoding=encoding)
                    else:
                        name = Path(str(item)).stem or str(item)
                        result[name] = str(item)
                else:
                    name = getattr(item, 'name', None)
                    if hasattr(item, 'read'):
                        content = item.read()
                        if hasattr(content, 'decode'):
                            content = content.decode(encoding)
                        result[name or f'item_{len(result)}'] = content
                    else:
                        result[name or f'item_{len(result)}'] = str(item)
            return result

        return sources

    def _maybe_read(self, value, encoding):
        if hasattr(value, 'read'):
            data = value.read()
            return data.decode(encoding) if hasattr(data, 'decode') else data
        if isinstance(value, (str, os.PathLike)):
            p = Path(value)
            if p.exists() and p.is_file():
                return p.read_text(encoding=encoding)
        return value

    def _read_dir(self, directory: Path, encoding: str):
        data = {}
        for p in sorted(directory.rglob('*')):
            if p.is_file():
                key = p.relative_to(directory).as_posix()
                data[key] = p.read_text(encoding=encoding)
        return data

    def _detect_engine(self, template: str):
        # Heuristic: if Jinja-like delimiters present, choose jinja2 if available
        if any(tok in template for tok in ('{{', '{%', '{#')):
            return 'jinja2' if _jinja2 is not None else 'format'
        return 'format'

    def _render_format(self, template: str, context: Mapping):
        # Safe .format rendering: missing keys remain unchanged
        class SafeDict(dict):
            def __missing__(self, key):
                return '{' + key + '}'
        return template.format_map(SafeDict(context))

    def _render_jinja2(self, template: str, context: Mapping, cfg: Mapping):
        loader = None
        searchpath = cfg.get('searchpath')
        if searchpath:
            if isinstance(searchpath, (str, os.PathLike)):
                searchpath = [searchpath]
            loader = _jinja2.FileSystemLoader(
                [str(Path(p)) for p in searchpath])

        env_kwargs = {
            'autoescape': cfg.get('autoescape', False),
            'trim_blocks': cfg.get('trim_blocks', True),
            'lstrip_blocks': cfg.get('lstrip_blocks', True),
            'loader': loader
        }
        env = _jinja2.Environment(**env_kwargs)
        filters = cfg.get('filters') or {}
        for name, func in filters.items():
            env.filters[name] = func

        # If a template_name is provided and loader exists, use it; else render from string
        template_name = cfg.get('template_name')
        if template_name and loader is not None:
            tpl = env.get_template(template_name)
        else:
            tpl = env.from_string(template)
        return tpl.render(**context)

    def _write_output(self, rendered: str, out, cfg):
        if hasattr(out, 'write'):
            out.write(rendered)
            return
        p = Path(out)
        p.parent.mkdir(parents=True, exist_ok=True)
        encoding = cfg.get('output_encoding', cfg.get('encoding', 'utf-8'))
        p.write_text(rendered, encoding=encoding)
