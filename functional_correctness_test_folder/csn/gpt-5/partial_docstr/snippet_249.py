import sys
from typing import Any, Callable, Dict, Iterable, Iterator, List, Mapping, Optional, Sequence, Tuple, Union, TextIO, BinaryIO


class Template:
    def __init__(self):
        '''Class instantiation
        '''
        self._default_item_template = "{content}"
        self._default_header = ""
        self._default_footer = ""
        self._default_separator = "\n"
        self._newline = False

    def _iter_sources(self, sources: Any) -> Iterator[Tuple[Optional[str], Any]]:
        if sources is None:
            return iter([])
        if isinstance(sources, dict):
            for k, v in sources.items():
                yield k, v
            return
        if isinstance(sources, (list, tuple, set)):
            for v in sources:
                yield None, v
            return
        # Single item
        yield None, sources

    def _normalize_item(self, name: Optional[str], item: Any) -> Dict[str, Any]:
        if isinstance(item, Mapping):
            data = dict(item)
            if name is not None and "name" not in data:
                data["name"] = name
            return data
        # For non-mapping, treat as content
        return {"name": name, "content": item}

    def _apply_transform(self, data: Dict[str, Any], transform: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]]) -> Dict[str, Any]:
        if transform is None:
            return data
        result = transform(data)
        if not isinstance(result, Mapping):
            # Coerce to dict with content if transform didn't return mapping
            return {"name": data.get("name"), "content": result}
        return dict(result)

    def _format(self, template: str, context: Dict[str, Any]) -> str:
        class SafeDict(dict):
            def __missing__(self, key):
                return "{" + key + "}"
        return template.format_map(SafeDict(context))

    def _coerce_stream(self, out: Union[TextIO, BinaryIO], encoding: Optional[str]) -> Tuple[Callable[[str], None], Callable[[], None]]:
        is_binary = "b" in getattr(out, "mode", "") or isinstance(
            getattr(out, "buffer", None), (type(None),))
        # Detect writable method
        write = getattr(out, "write", None)
        if write is None:
            def _noop_close():
                return

            def _noop_write(_: str):
                return
            return _noop_write, _noop_close

        if isinstance(out, (sys.stdout.__class__,)) and hasattr(out, "encoding"):
            enc = out.encoding or encoding or "utf-8"
        else:
            enc = encoding or "utf-8"

        if isinstance(out, BinaryIO.__args__) if hasattr(BinaryIO, "__args__") else False:
            is_binary = True

        if hasattr(out, "encoding"):
            is_binary = False

        if is_binary:
            def _bwrite(s: str):
                out.write(s.encode(enc, errors="replace"))
            return _bwrite, getattr(out, "flush", lambda: None)
        else:
            def _twrite(s: str):
                out.write(s)
            return _twrite, getattr(out, "flush", lambda: None)

    def render(self, sources, config, out=sys.stdout):
        '''Render the documentation as defined in config Object
        '''
        if config is None:
            config = {}
        if not isinstance(config, Mapping):
            raise TypeError("config must be a mapping/dict")

        header = config.get("header", self._default_header)
        footer = config.get("footer", self._default_footer)
        item_template = config.get(
            "item_template", self._default_item_template)
        separator = config.get("separator", self._default_separator)
        context = dict(config.get("context", {})) if isinstance(
            config.get("context", {}), Mapping) else {}
        transform = config.get("transform", None)
        max_items = config.get("max_items", None)
        sort_key = config.get("sort", None)
        reverse = False
        encoding = config.get("encoding", None)
        append_newline = config.get("newline", self._newline)

        items: List[Tuple[Optional[str], Any]] = list(
            self._iter_sources(sources))

        if isinstance(sort_key, bool):
            if sort_key:
                items.sort(key=lambda kv: (
                    "" if kv[0] is None else str(kv[0])))
        elif callable(sort_key):
            items.sort(key=lambda kv: sort_key(kv[1]))
        elif isinstance(sort_key, str):
            key_name = sort_key
            items.sort(key=lambda kv: self._normalize_item(
                kv[0], kv[1]).get(key_name, ""))
        elif isinstance(sort_key, dict):
            key_name = sort_key.get("key")
            reverse = bool(sort_key.get("reverse", False))
            if callable(key_name):
                items.sort(key=lambda kv: key_name(kv[1]), reverse=reverse)
            elif isinstance(key_name, str):
                items.sort(key=lambda kv: self._normalize_item(
                    kv[0], kv[1]).get(key_name, ""), reverse=reverse)

        if isinstance(max_items, int) and max_items >= 0:
            items = items[:max_items]

        rendered_parts: List[str] = []

        if header:
            rendered_parts.append(self._format(header, context))

        for name, raw in items:
            data = self._normalize_item(name, raw)
            data = self._apply_transform(
                data, transform) if callable(transform) else data
            merged = {**context, **data}
            rendered_parts.append(self._format(item_template, merged))

        if footer:
            rendered_parts.append(self._format(footer, context))

        rendered = separator.join(rendered_parts)
        if append_newline and (not rendered.endswith("\n")):
            rendered += "\n"

        write, flush = self._coerce_stream(out, encoding)
        write(rendered)
        flush()
        return rendered
