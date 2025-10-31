
class Merger:

    def merge_extends(self, target, extends, inherit_key='inherit', inherit=False):
        if not isinstance(target, dict) or not isinstance(extends, dict):
            return target

        for key, value in extends.items():
            if key == inherit_key and inherit:
                continue
            if key in target:
                if isinstance(target[key], dict) and isinstance(value, dict):
                    self.merge_extends(
                        target[key], value, inherit_key, inherit)
                else:
                    target[key] = value
            else:
                target[key] = value
        return target

    def merge_sources(self, datas):
        if not datas:
            return {}

        merged = {}
        for data in datas:
            if not isinstance(data, dict):
                continue
            merged = self.merge_extends(merged, data)
        return merged

    def merge_configs(self, config, datas):
        '''Merge configs files
        '''
        if not isinstance(config, dict):
            return self.merge_sources(datas) if datas else {}

        merged_config = config.copy()
        for data in datas:
            if isinstance(data, dict):
                merged_config = self.merge_extends(merged_config, data)
        return merged_config
