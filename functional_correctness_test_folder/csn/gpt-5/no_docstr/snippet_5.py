from typing import Any, Iterable


class ExtensionLoaderMixin:

    def __init__(self, *, context: dict[str, Any] | None = None, **kwargs: Any) -> None:
        # Be cooperative in multiple-inheritance scenarios
        try:
            super().__init__(**kwargs)  # type: ignore[misc]
        except TypeError:
            # Parent may not accept kwargs or have no __init__
            pass

        self._context: dict[str, Any] = dict(context) if context else {}
        self.extensions: list[str] = self._read_extensions(self._context)

    def _read_extensions(self, context: dict[str, Any]) -> list[str]:
        def to_list(value: Any) -> list[str]:
            if value is None:
                return []
            if isinstance(value, str):
                parts = [p.strip()
                         for p in value.replace("\n", " ").split(",")]
                flat: list[str] = []
                for part in parts:
                    if not part:
                        continue
                    flat.extend([x for x in part.split() if x])
                return flat
            if isinstance(value, dict):
                raise TypeError("Extensions cannot be provided as a dict.")
            if isinstance(value, Iterable):
                out: list[str] = []
                for v in value:
                    s = str(v).strip()
                    if s:
                        out.append(s)
                return out
            return [str(value).strip()] if str(value).strip() else []

        # Prefer 'extensions', fall back to 'extension'
        raw = None
        if "extensions" in context:
            raw = context.get("extensions")
        elif "extension" in context:
            raw = context.get("extension")

        items = to_list(raw)
        # Deduplicate while preserving order
        seen: set[str] = set()
        result: list[str] = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
