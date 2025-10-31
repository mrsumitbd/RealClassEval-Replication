
class Merger:

    def merge_extends(self, target, extends, inherit_key='inherit', inherit=False):
        if inherit:
            for key, value in extends.items():
                if key == inherit_key and isinstance(value, list):
                    for inherit_item in value:
                        if inherit_item in target:
                            target.update(target[inherit_item])
                else:
                    if key not in target:
                        target[key] = value
                    elif isinstance(target[key], dict) and isinstance(value, dict):
                        self.merge_extends(
                            target[key], value, inherit_key, inherit)
        else:
            target.update(extends)
        return target

    def merge_sources(self, datas):
        merged_data = {}
        for data in datas:
            self.merge_extends(merged_data, data)
        return merged_data

    def merge_configs(self, config, datas):
        for data in datas:
            self.merge_extends(config, data, inherit=True)
        return config
