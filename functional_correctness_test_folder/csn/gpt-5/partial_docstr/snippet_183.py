class Reader:
    '''
    The reader provides integration with cache.
    @ivar options: An options object.
    @type options: Options
    '''

    def __init__(self, options):
        self.options = options

    def mangle(self, name, x):
        import json
        import hashlib

        if not isinstance(name, str) or not name:
            raise ValueError("name must be a non-empty string")

        # Determine optional prefix/namespace from options
        prefix = ""
        for attr in ("cache_prefix", "prefix", "namespace", "cache_namespace"):
            val = getattr(self.options, attr, None)
            if isinstance(val, str) and val:
                prefix = val
                break

        # Serialize x in a stable way and hash to form a compact key
        try:
            payload = json.dumps(
                x, sort_keys=True, separators=(",", ":"), default=str)
        except TypeError:
            payload = repr(x)

        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()

        parts = []
        if prefix:
            parts.append(prefix)
        parts.append(name)
        parts.append(digest)
        return ":".join(parts)
