
import copy


class Merger:

    def merge_extends(self, target, extends, inherit_key='inherit', inherit=False):
        if inherit or (inherit_key in target and target[inherit_key]):
            for key, value in extends.items():
                if key not in target:
                    target[key] = value
                elif isinstance(target[key], dict) and isinstance(value, dict):
                    target[key] = self.merge_extends(
                        target[key], value, inherit_key, inherit)
                elif isinstance(target[key], list) and isinstance(value, list):
                    target[key].extend(value)
        return target

    def merge_sources(self, datas):
        result = {}
        for data in datas:
            result = self.merge_extends(result, data)
        return result

    def merge_configs(self, config, datas):
        '''Merge configs files
        '''
        merged_data = self.merge_sources(datas)
        return self.merge_extends(copy.deepcopy(config), merged_data)
