
class Merger:

    def merge_extends(self, target, extends, inherit_key='inherit', inherit=False):
        """
        Merge 'extends' dict into 'target' dict.
        If 'inherit' is True or target[inherit_key] is True, values from 'extends' are merged into 'target'.
        If both have a dict at a key, merge recursively.
        """
        if not isinstance(target, dict) or not isinstance(extends, dict):
            return target
        do_inherit = inherit or target.get(inherit_key, False)
        if not do_inherit:
            return target
        for k, v in extends.items():
            if k == inherit_key:
                continue
            if k in target and isinstance(target[k], dict) and isinstance(v, dict):
                target[k] = self.merge_extends(
                    target[k], v, inherit_key, inherit)
            elif k not in target:
                target[k] = v
        return target

    def merge_sources(self, datas):
        """
        Merge a list of dicts into one dict.
        Later dicts override earlier ones.
        If both have a dict at a key, merge recursively.
        """
        result = {}
        for data in datas:
            for k, v in data.items():
                if (
                    k in result
                    and isinstance(result[k], dict)
                    and isinstance(v, dict)
                ):
                    result[k] = self.merge_sources([result[k], v])
                else:
                    result[k] = v
        return result

    def merge_configs(self, config, datas):
        """
        Merge a list of dicts (datas) into config.
        Later dicts override earlier ones.
        If both have a dict at a key, merge recursively.
        """
        merged = config.copy()
        for data in datas:
            for k, v in data.items():
                if (
                    k in merged
                    and isinstance(merged[k], dict)
                    and isinstance(v, dict)
                ):
                    merged[k] = self.merge_configs(merged[k], [v])
                else:
                    merged[k] = v
        return merged
