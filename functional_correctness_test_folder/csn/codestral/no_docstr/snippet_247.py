
class Merger:

    def merge_extends(self, target, extends, inherit_key='inherit', inherit=False):

        if not isinstance(target, dict) or not isinstance(extends, dict):
            raise ValueError("Both target and extends must be dictionaries")

        for key, value in extends.items():
            if key == inherit_key:
                if inherit:
                    target.update(value)
            else:
                if key in target:
                    if isinstance(target[key], dict) and isinstance(value, dict):
                        self.merge_extends(
                            target[key], value, inherit_key, inherit)
                    elif isinstance(target[key], list) and isinstance(value, list):
                        target[key].extend(value)
                    else:
                        target[key] = value
                else:
                    target[key] = value

    def merge_sources(self, datas):

        if not isinstance(datas, list):
            raise ValueError("datas must be a list of dictionaries")

        merged_data = {}
        for data in datas:
            if not isinstance(data, dict):
                raise ValueError("Each element in datas must be a dictionary")
            self.merge_extends(merged_data, data)
        return merged_data

    def merge_configs(self, config, datas):

        if not isinstance(config, dict) or not isinstance(datas, list):
            raise ValueError(
                "config must be a dictionary and datas must be a list of dictionaries")

        merged_data = self.merge_sources(datas)
        self.merge_extends(config, merged_data, inherit=True)
        return config
