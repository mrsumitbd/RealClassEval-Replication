
class Merger:
    '''Provide tool to merge elements
    '''

    def merge_extends(self, target, extends, inherit_key='inherit', inherit=False):
        '''Merge extended dicts
        '''
        if inherit:
            for key, value in extends.items():
                if isinstance(value, dict) and inherit_key in value:
                    target[key] = self.merge_extends(target.get(
                        key, {}), value[inherit_key], inherit_key, inherit)
                else:
                    target[key] = value
        else:
            target.update(extends)
        return target

    def merge_sources(self, datas):
        '''Merge sources files
        '''
        merged_data = {}
        for data in datas:
            merged_data.update(data)
        return merged_data

    def merge_configs(self, config, datas):
        '''Merge configs files
        '''
        merged_config = config.copy()
        for data in datas:
            self.merge_extends(merged_config, data, inherit=True)
        return merged_config
