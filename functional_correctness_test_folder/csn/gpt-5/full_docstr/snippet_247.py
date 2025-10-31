class Merger:
    '''Provide tool to merge elements
    '''

    def _deepcopy(self, obj):
        # Lightweight deepcopy for common JSON-like structures
        if isinstance(obj, dict):
            return {k: self._deepcopy(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._deepcopy(v) for v in obj]
        return obj

    def _merge(self, base, override, inherit, inherit_key):
        # If override explicitly disables inheritance at this node, replace entirely
        if isinstance(override, dict):
            explicit = override.get(inherit_key, None)
            if explicit is False:
                # Replace entirely, removing the inherit key
                return {k: self._deepcopy(v) for k, v in override.items() if k != inherit_key}

        # Dict merge
        if isinstance(base, dict) and isinstance(override, dict):
            result = {}
            # Start from base
            for k, v in base.items():
                result[k] = self._deepcopy(v)
            # Merge override
            for k, v in override.items():
                if k == inherit_key:
                    continue
                if k in result:
                    result[k] = self._merge(result[k], v, inherit, inherit_key)
                else:
                    result[k] = self._deepcopy(v)
            return result

        # List handling
        if isinstance(base, list) and isinstance(override, list):
            if inherit:
                return self._deepcopy(base) + self._deepcopy(override)
            return self._deepcopy(override)

        # Different types or scalars: override wins
        return self._deepcopy(override)

    def merge_extends(self, target, extends, inherit_key='inherit', inherit=False):
        '''Merge extended dicts
        '''
        # Normalize inputs
        tgt = {} if target is None else self._deepcopy(target)
        bases = []
        if extends is None:
            bases = []
        elif isinstance(extends, (list, tuple)):
            bases = list(extends)
        else:
            bases = [extends]

        # Start with empty base and merge all extends in order
        result = {}
        for base in bases:
            if base is None:
                continue
            result = self._merge(result, base, True, inherit_key)

        # If target has explicit inherit directive at the root, honor it
        root_inherit = inherit
        if isinstance(tgt, dict) and inherit_key in tgt:
            # If root explicitly sets inherit False, replace base entirely with target (minus inherit key)
            if tgt.get(inherit_key) is False:
                return {k: self._deepcopy(v) for k, v in tgt.items() if k != inherit_key}
            # If True, ensure deep merge
            root_inherit = True
            # Remove inherit directive from final result
            tgt = {k: v for k, v in tgt.items() if k != inherit_key}

        # Merge target over the accumulated base
        result = self._merge(result, tgt, root_inherit, inherit_key)
        return result

    def merge_sources(self, datas):
        '''Merge sources files
        '''
        if not datas:
            return {}
        result = {}
        for d in datas:
            if d is None:
                continue
            result = self._merge(result, d, True, 'inherit')
        return result

    def merge_configs(self, config, datas):
        '''Merge configs files
        '''
        # First merge all source data as base, then overlay the config
        base = self.merge_sources(datas)
        return self.merge_extends(config or {}, base, inherit_key='inherit', inherit=True)
