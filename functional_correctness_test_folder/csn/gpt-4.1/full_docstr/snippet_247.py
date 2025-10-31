
class Merger:
    '''Provide tool to merge elements
    '''

    def merge_extends(self, target, extends, inherit_key='inherit', inherit=False):
        '''Merge extended dicts
        '''
        if not isinstance(target, dict):
            return target
        result = {}
        # If inherit is True, merge extends first, then target overrides
        if inherit:
            for k, v in extends.items():
                if k == inherit_key:
                    continue
                result[k] = v
            for k, v in target.items():
                if k == inherit_key:
                    continue
                if k in result and isinstance(result[k], dict) and isinstance(v, dict):
                    result[k] = self.merge_extends(
                        v, result[k], inherit_key, inherit)
                else:
                    result[k] = v
        else:
            # target overrides extends
            for k, v in target.items():
                if k == inherit_key:
                    continue
                result[k] = v
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
        '''Merge sources files
        '''
        if not datas:
            return {}
        result = {}
        for data in datas:
            if not isinstance(data, dict):
                continue
            for k, v in data.items():
                if k in result and isinstance(result[k], dict) and isinstance(v, dict):
                    result[k] = self.merge_sources([result[k], v])
                else:
                    result[k] = v
        return result

    def merge_configs(self, config, datas):
        '''Merge configs files
        '''
        merged = self.merge_sources(datas)
        if not isinstance(config, dict):
            return merged
        for k, v in config.items():
            if k in merged and isinstance(merged[k], dict) and isinstance(v, dict):
                merged[k] = self.merge_configs(v, [merged[k]])
            else:
                merged[k] = v
        return merged
