class Template:
    def __init__(self, name, versions):
        self.name = name
        # Normalize versions into an ordered dict: name -> version_obj
        self._versions = {}
        if versions is None:
            versions = []
        if isinstance(versions, dict):
            for k, v in versions.items():
                self._versions[str(k)] = v
        else:
            for v in versions:
                key = None
                # Try to infer a version name from common attributes or the value itself
                for attr in ("name", "version", "ver_name", "id"):
                    if hasattr(v, attr):
                        key = getattr(v, attr)
                        break
                if key is None:
                    key = str(v)
                self._versions[str(key)] = v

    def _parse_semver_like(self, s):
        # Strip common prefixes (e.g., 'v1.2.3') and suffixes
        s = str(s).strip()
        if s.startswith(("v", "V")):
            s = s[1:]
        # Split by dots, dashes; keep only numeric leading parts
        parts = []
        for token in s.replace("-", ".").split("."):
            if token.isdigit():
                parts.append(int(token))
            else:
                # Stop at first non-numeric token; semantic versions beyond this are ignored
                break
        if not parts:
            raise ValueError("not parseable")
        return tuple(parts)

    def _latest_by_semver_or_insertion(self):
        if not self._versions:
            return None
        keys = list(self._versions.keys())
        parsed = {}
        for k in keys:
            try:
                parsed[k] = self._parse_semver_like(k)
            except Exception:
                parsed = None
                break
        if parsed is None or not parsed:
            # Fallback to insertion order: pick last inserted
            last_key = next(reversed(self._versions))
            return self._versions[last_key]
        # Choose the key with the maximum semantic tuple; tie-breaker by key string
        best_key = max(parsed.keys(), key=lambda k: (parsed[k], k))
        return self._versions[best_key]

    def get_version(self, ver_name=None):
        '''
        Get the given version for this template, or the latest
        Args:
            ver_name (str or None): Version to retieve, None for the latest
        Returns:
            TemplateVersion: The version matching the given name or the latest
                one
        '''
        if ver_name is None:
            return self.get_latest_version()
        key = str(ver_name)
        if key not in self._versions:
            raise KeyError(
                f"Version '{ver_name}' not found for template '{self.name}'.")
        return self._versions[key]

    def get_latest_version(self):
        return self._latest_by_semver_or_insertion()
