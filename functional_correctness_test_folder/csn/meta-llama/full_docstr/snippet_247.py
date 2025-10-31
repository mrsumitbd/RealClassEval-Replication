
import copy


class Merger:
    '''Provide tool to merge elements
    '''

    def merge_extends(self, target, extends, inherit_key='inherit', inherit=False):
        '''Merge extended dicts
        '''
        if inherit_key in target and target[inherit_key]:
            for extend in target[inherit_key]:
                if extend in extends:
                    extended_target = copy.deepcopy(extends[extend])
                    if inherit:
                        self.merge_extends(
                            extended_target, extends, inherit_key, inherit)
                    target = self._merge_dict(extended_target, target)
        return target

    def _merge_dict(self, source, target):
        for key, value in source.items():
            if isinstance(value, dict) and key in target:
                target[key] = self._merge_dict(value, target[key])
            else:
                target[key] = value
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
        merged_config = copy.deepcopy(config)
        for data in datas:
            merged_config = self.merge_extends(
                merged_config, data, inherit=True)
        return merged_config
