class Merger:

    def merge_extends(self, target, extends, inherit_key='inherit', inherit=False):
        from copy import deepcopy

        def _merge_dicts(a, b, inherit_flag):
            result = deepcopy(a) if isinstance(a, dict) else {}
            if not isinstance(b, dict):
                return deepcopy(b)

            # Determine local inherit
            local_inherit = b.get(
                inherit_key, result.get(inherit_key, inherit_flag))
            local_inherit = bool(local_inherit)

            for k, b_val in b.items():
                if k == inherit_key:
                    continue
                a_val = result.get(k, None)

                if isinstance(a_val, dict) and isinstance(b_val, dict):
                    result[k] = _merge_dicts(a_val, b_val, local_inherit)
                elif isinstance(a_val, list) and isinstance(b_val, list):
                    if local_inherit:
                        result[k] = a_val + b_val
                    else:
                        result[k] = deepcopy(b_val)
                else:
                    result[k] = deepcopy(b_val)

            # Remove inherit directive if present
            if inherit_key in result:
                result = dict(result)
                result.pop(inherit_key, None)

            return result

        target = target or {}
        extends = extends or {}
        return _merge_dicts(target, extends, inherit)

    def merge_sources(self, datas):
        from copy import deepcopy
        result = {}
        if not datas:
            return result
        for data in datas:
            if not isinstance(data, dict):
                continue
            result = self.merge_extends(result, data)
        return result

    def merge_configs(self, config, datas):
        '''Merge configs files
        '''
        from copy import deepcopy

        result = deepcopy(config) if isinstance(config, dict) else {}
        # Handle extends in base config first
        if isinstance(result, dict) and 'extends' in result:
            parents = result.pop('extends')
            if isinstance(parents, list):
                for p in parents:
                    if isinstance(p, dict):
                        result = self.merge_extends(result, p)
            elif isinstance(parents, dict):
                result = self.merge_extends(result, parents)

        # Then merge provided data sources
        if datas:
            if isinstance(datas, list):
                for d in datas:
                    if isinstance(d, dict):
                        result = self.merge_extends(result, d)
            elif isinstance(datas, dict):
                result = self.merge_extends(result, datas)

        return result
