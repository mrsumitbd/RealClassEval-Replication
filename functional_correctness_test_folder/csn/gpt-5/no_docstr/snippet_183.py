class Reader:
    def __init__(self, options):
        # Normalize options
        if options is None:
            options = {}
        elif isinstance(options, str):
            options = {"template": options}
        elif not isinstance(options, dict):
            # Fallback to string template with default representation
            options = {"template": "{name}_{x}"}

        self.template = options.get("template")

        # Name transformations: lower, upper, title, snake, kebab, camel (basic)
        self.transform = options.get("transform")
        self.prefix = options.get("prefix", "")
        self.suffix = options.get("suffix", "")
        self.sep = options.get("sep", "_")

        # x formatting
        self.pad = options.get("pad")  # int or None
        self.base = options.get("base")  # 2, 8, 10, 16 or 'bin','oct','hex'
        self.base = {"bin": 2, "oct": 8, "hex": 16}.get(self.base, self.base)
        if self.base not in (None, 2, 8, 10, 16):
            self.base = None

        # Hash options
        self.use_hash = bool(options.get("hash", False))
        self.hash_len = int(options.get("hash_len", 8))
        if self.hash_len < 0:
            self.hash_len = 0

        # Limit length
        self.max_length = options.get("max_length")
        try:
            if self.max_length is not None:
                self.max_length = int(self.max_length)
                if self.max_length <= 0:
                    self.max_length = None
        except Exception:
            self.max_length = None

    def mangle(self, name, x):
        name = "" if name is None else str(name)

        # Apply name transformation
        tname = self._transform_name(name)

        # Format x
        x_str = self._format_x(x)

        # If template is provided, use it
        if self.template:
            try:
                result = self.template.format(name=tname, x=x_str)
            except Exception:
                # Fallback to simple concatenation if template fails
                result = self._assemble(tname, x_str)
        else:
            result = self._assemble(tname, x_str)

        # Add hash if requested
        if self.use_hash:
            h = self._short_hash(f"{name}|{x}")
            if result:
                result = f"{result}{self.sep}{h}" if self.sep else f"{result}{h}"
            else:
                result = h

        # Enforce max length (prefer trimming within the name part)
        if self.max_length is not None and len(result) > self.max_length:
            result = self._truncate_preserving_suffix(result, self.max_length)

        return result

    def _transform_name(self, name):
        mode = (self.transform or "").lower()
        if not mode:
            return name
        if mode == "lower":
            return name.lower()
        if mode == "upper":
            return name.upper()
        if mode == "title":
            return name.title()
        if mode == "snake":
            return self._to_delimited(name, "_")
        if mode == "kebab":
            return self._to_delimited(name, "-")
        if mode == "camel":
            parts = self._split_words(name)
            if not parts:
                return ""
            head = parts[0].lower()
            tail = "".join(p.capitalize() for p in parts[1:])
            return head + tail
        return name

    def _format_x(self, x):
        # Try integer formatting if possible
        as_int = self._to_int_or_none(x)
        if as_int is not None:
            # base formatting
            if self.base == 2:
                out = format(as_int, "b")
            elif self.base == 8:
                out = format(as_int, "o")
            elif self.base == 16:
                out = format(as_int, "x")
            else:
                out = str(as_int)
            # padding
            if isinstance(self.pad, int) and self.pad > 0:
                out = out.zfill(self.pad)
            return out
        # Non-integer, just string
        return "" if x is None else str(x)

    def _assemble(self, tname, x_str):
        parts = []
        if self.prefix:
            parts.append(self.prefix)
        if tname:
            parts.append(tname)
        if x_str != "":
            parts.append(str(x_str))
        if self.suffix:
            parts.append(self.suffix)
        if not parts:
            return ""
        if self.sep is None:
            return "".join(parts)
        return self.sep.join(parts)

    def _short_hash(self, s):
        import hashlib
        digest = hashlib.sha1(s.encode("utf-8")).hexdigest()
        return digest[: self.hash_len] if self.hash_len else ""

    def _truncate_preserving_suffix(self, s, limit):
        if len(s) <= limit:
            return s
        # Try to preserve the last segment after sep
        if not self.sep:
            return s[:limit]
        sep = self.sep
        # If no sep present, simple truncate
        if sep not in s:
            return s[:limit]
        parts = s.split(sep)
        # Keep last part, trim the front aggregating with sep
        tail = parts[-1]
        # Ensure tail fits; if not, hard truncate tail
        if len(tail) >= limit:
            return tail[-limit:]
        # Space left for head + separators
        remaining = limit - len(tail) - len(sep)
        if remaining <= 0:
            return tail[-limit:]
        head = sep.join(parts[:-1])
        if len(head) > remaining:
            head = head[:remaining]
            # Avoid trailing partial separator by trimming to not end with sep
            if head.endswith(sep):
                head = head[: -len(sep)]
        return f"{head}{sep}{tail}"

    def _to_int_or_none(self, x):
        try:
            if isinstance(x, bool):
                return int(x)
            if isinstance(x, (int,)):
                return int(x)
            if isinstance(x, (float,)) and x.is_integer():
                return int(x)
            if isinstance(x, str):
                xs = x.strip().lower()
                # Auto-detect base prefixes
                if xs.startswith("0x"):
                    return int(xs, 16)
                if xs.startswith("0o"):
                    return int(xs, 8)
                if xs.startswith("0b"):
                    return int(xs, 2)
                return int(xs, 10)
            return None
        except Exception:
            return None

    def _split_words(self, s):
        # Split on non-alnum and camelCase boundaries
        import re
        s = s.strip()
        if not s:
            return []
        # Replace separators with space
        s = re.sub(r"[^A-Za-z0-9]+", " ", s)
        # Split camelCase/PascalCase
        s = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", s)
        parts = [p for p in s.split() if p]
        return parts

    def _to_delimited(self, s, delim):
        parts = self._split_words(s)
        if delim == "_":
            return "_".join(p.lower() for p in parts)
        if delim == "-":
            return "-".join(p.lower() for p in parts)
        return delim.join(parts)
