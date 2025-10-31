
class Merger:

    def merge_extends(self, target, extends, inherit_key='inherit', inherit=False):
        if not isinstance(target, dict) or not isinstance(extends, dict):
            return target

        for key, value in extends.items():
            if key == inherit_key and inherit:
                continue
            if key not in target:
                target[key] = value
            else:
                if isinstance(value, dict) and isinstance(target[key], dict):
                    self.merge_extends(
                        target[key], value, inherit_key, inherit)
                else:
                    target[key] = value
        return target

    def merge_sources(self, datas):
        if not datas:
            return {}

        result = {}
        for data in datas:
            if isinstance(data, dict):
                result = self.merge_extends(result, data)
        return result

    def merge_configs(self, config, datas):
        if not isinstance(config, dict):
            return self.merge_sources(datas)

        merged = self.merge_sources(datas)
        return self.merge_extends(config, merged)
