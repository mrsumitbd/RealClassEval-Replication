
class Merger:

    def merge_extends(self, target, extends, inherit_key='inherit', inherit=False):
        """
        Merge 'extends' dict into 'target' dict.
        If 'inherit' is True or target[inherit_key] is True, recursively merge.
        """
        if not isinstance(target, dict) or not isinstance(extends, dict):
            return target

        # Determine if we should inherit
        do_inherit = inherit or target.get(inherit_key, False)
        result = target.copy()
        if do_inherit:
            for k, v in extends.items():
                if k == inherit_key:
                    continue
                if k in result and isinstance(result[k], dict) and isinstance(v, dict):
                    result[k] = self.merge_extends(
                        result[k], v, inherit_key, inherit)
                elif k not in result:
                    result[k] = v
        return result

    def merge_sources(self, datas):
        """
        Merge a list of dicts into one dict, later dicts override earlier ones.
        """
        result = {}
        for data in datas:
            if isinstance(data, dict):
                result.update(data)
        return result

    def merge_configs(self, config, datas):
        '''Merge configs files'''
        # datas: list of dicts to merge, config: base dict
        merged = self.merge_sources(datas)
        # Now merge config with merged, config has lower priority
        result = config.copy() if isinstance(config, dict) else {}
        result.update(merged)
        return result
