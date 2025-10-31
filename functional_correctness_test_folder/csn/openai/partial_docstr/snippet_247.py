
class Merger:
    def _deep_merge(self, target, source, inherit_key='inherit', inherit=False):
        """
        Recursively merge `source` into `target`. If `inherit` is True, nested
        dictionaries are merged; otherwise, nested dictionaries are replaced.
        """
        for key, value in source.items():
            if key == inherit_key:
                continue
            if key in target:
                if isinstance(target[key], dict) and isinstance(value, dict):
                    if inherit:
                        self._deep_merge(
                            target[key], value, inherit_key, inherit)
                    else:
                        target[key] = value
                else:
                    target[key] = value
            else:
                target[key] = value

    def merge_extends(self, target, extends, inherit_key='inherit', inherit=False):
        """
        Merge a list of dictionaries (`extends`) into `target`. If a dictionary
        contains the key `inherit_key` set to a truthy value, its contents are
        merged into `target`. The `inherit` flag controls whether nested
        dictionaries are merged recursively.
        """
        if not isinstance(extends, (list, tuple)):
            extends = [extends]
        for src in extends:
            if not isinstance(src, dict):
                continue
            if src.get(inherit_key):
                self._deep_merge(target, src, inherit_key, inherit)
            else:
                # If not inheriting, simply overwrite or add keys
                for k, v in src.items():
                    if k != inherit_key:
                        target[k] = v
        return target

    def merge_sources(self, datas):
        """
        Merge a sequence of dictionaries into a single dictionary. The merge
        is shallow; nested dictionaries are replaced.
        """
        result = {}
        for data in datas:
            if isinstance(data, dict):
                self.merge_extends(result, data, inherit=False)
        return result

    def merge_configs(self, config, datas):
        """
        Merge a configuration dictionary into each dictionary in `datas`.
        The merge is deep (recursive) and respects the `inherit` flag.
        Returns a list of merged dictionaries.
        """
        merged = []
        for data in datas:
            if not isinstance(data, dict):
                continue
            # Create a copy to avoid mutating the original
            copy = dict(data)
            self.merge_extends(
                copy, config, inherit_key='inherit', inherit=True)
            merged.append(copy)
        return merged
