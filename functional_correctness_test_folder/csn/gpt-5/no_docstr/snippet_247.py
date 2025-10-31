class Merger:
    def _deepcopy(self, obj):
        import copy
        return copy.deepcopy(obj)

    def _merge_lists(self, base, child):
        seen = set()
        result = []
        for item in base + child:
            key = id(item)
            # For hashable values, use the value; otherwise fallback to id
            try:
                key = (True, item)
            except Exception:
                key = (False, id(item))
            if key in seen:
                continue
            seen.add(key)
            result.append(item)
        return result

    def merge_extends(self, target, extends, inherit_key='inherit', inherit=False):
        if target is None and extends is None:
            return None
        if not isinstance(target, dict) and not isinstance(extends, dict):
            return target if target is not None else extends
        target = {} if target is None else target
        extends = {} if extends is None else extends

        result = {}
        keys = set(extends.keys()) | set(target.keys())

        for key in keys:
            child_present = key in target
            base_present = key in extends

            child_val = self._deepcopy(target[key]) if child_present else None
            base_val = self._deepcopy(extends[key]) if base_present else None

            local_inherit = bool(inherit)
            # If child is a dict and contains inherit flag, use it and remove the flag from final value
            if isinstance(child_val, dict) and inherit_key in child_val:
                inherit_flag = bool(child_val.get(inherit_key))
                # Remove the inherit key for the resultant merged value
                child_val = {k: self._deepcopy(
                    v) for k, v in child_val.items() if k != inherit_key}
                local_inherit = local_inherit or inherit_flag

            if child_present:
                if base_present and local_inherit:
                    # Merge based on types
                    if isinstance(base_val, dict) and isinstance(child_val, dict):
                        merged = self.merge_extends(
                            child_val, base_val, inherit_key=inherit_key, inherit=local_inherit)
                    elif isinstance(base_val, list) and isinstance(child_val, list):
                        merged = self._merge_lists(base_val, child_val)
                    else:
                        merged = child_val
                else:
                    merged = child_val
            else:
                # child not present
                if base_present and local_inherit:
                    merged = base_val
                else:
                    continue  # skip key entirely

            result[key] = merged

        return result

    def merge_sources(self, datas):
        def deep_merge(a, b):
            # merge b over a
            if a is None:
                return self._deepcopy(b)
            if b is None:
                return self._deepcopy(a)
            if isinstance(a, dict) and isinstance(b, dict):
                res = {k: self._deepcopy(v) for k, v in a.items()}
                for k, v in b.items():
                    if k in res:
                        res[k] = deep_merge(res[k], v)
                    else:
                        res[k] = self._deepcopy(v)
                return res
            else:
                return self._deepcopy(b)

        result = {}
        if datas is None:
            return result
        for d in datas:
            if d is None:
                continue
            if not isinstance(d, dict):
                continue
            result = deep_merge(result, d)
        return result

    def merge_configs(self, config, datas):
        merged_sources = self.merge_sources(datas)
        base = config if isinstance(config, dict) else {}
        # Include base keys by default; child can suppress inheritance per-branch
        return self.merge_extends(merged_sources, base, inherit_key='inherit', inherit=True)
