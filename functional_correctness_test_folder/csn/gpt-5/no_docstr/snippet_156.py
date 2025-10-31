class SimpleService:
    def __init__(self, service_node):
        self._node = service_node
        self.name = None
        self.type = None
        self.tags = set()
        self.metadata = {}

        if service_node is None:
            return

        # Extract name
        self.name = self._extract_value(
            service_node, ["name", "service_name", "id"])

        # Extract type
        self.type = self._extract_value(
            service_node, ["type", "service_type", "kind"])

        # Extract tags
        tags_val = self._extract_value(
            service_node, ["tags", "labels", "roles"])
        if isinstance(tags_val, (list, tuple, set)):
            self.tags = {str(t).strip().lower()
                         for t in tags_val if t is not None}
        elif isinstance(tags_val, str):
            # Split by common separators
            parts = [p.strip() for p in tags_val.replace(",", " ").split()]
            self.tags = {p.lower() for p in parts if p}

        # Capture remaining metadata if dict-like
        if isinstance(service_node, dict):
            self.metadata = dict(service_node)
        else:
            # collect simple attributes
            for attr in dir(service_node):
                if attr.startswith("_"):
                    continue
                try:
                    val = getattr(service_node, attr)
                except Exception:
                    continue
                if callable(val):
                    continue
                self.metadata[attr] = val

    def is_resolver(self):
        node = self._node
        if node is None:
            return False

        # Explicit boolean flags
        for key in ("resolver", "is_resolver", "isResolver", "dns_resolver", "dnsResolver"):
            val = self._extract_value(node, [key])
            if isinstance(val, bool):
                return val
            if isinstance(val, str):
                lv = val.strip().lower()
                if lv in ("true", "yes", "1"):
                    return True
                if lv in ("false", "no", "0"):
                    return False

        # Type-based inference
        t = (self.type or "").strip().lower()
        if t in {"resolver", "dns", "dns-resolver", "dns_resolver", "name-service", "nameservice"}:
            return True

        # Tag-based inference
        tags = self.tags
        if {"resolver", "dns", "dns-resolver", "dns_resolver"} & tags:
            return True

        # Name-based heuristic
        n = (self.name or "").strip().lower()
        if any(k in n for k in ("resolver", "dns")):
            return True

        # Metadata hints
        for key in ("port", "protocol", "endpoint"):
            val = self.metadata.get(key)
            if key == "port" and str(val).isdigit():
                # common DNS port
                if int(val) == 53:
                    return True
            if key == "protocol" and isinstance(val, str) and val.strip().lower() in {"dns", "udp53"}:
                return True
            if key == "endpoint" and isinstance(val, str) and ":53" in val:
                return True

        return False

    @staticmethod
    def _extract_value(source, keys, default=None):
        for key in keys:
            # dict-like
            if isinstance(source, dict) and key in source:
                return source[key]
            # attribute-like
            try:
                if hasattr(source, key):
                    return getattr(source, key)
            except Exception:
                pass
            # case-insensitive dict keys
            if isinstance(source, dict):
                for k in source.keys():
                    try:
                        if str(k).lower() == str(key).lower():
                            return source[k]
                    except Exception:
                        continue
        return default
