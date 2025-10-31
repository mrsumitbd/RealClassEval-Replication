
class Merger:

    def merge_extends(self, target, extends, inherit_key='inherit', inherit=False):
        """Recursively merge target dictionary with its extends."""
        if isinstance(target, dict) and isinstance(extends, dict):
            for key, value in extends.items():
                if key == inherit_key:
                    inherit = value
                elif key not in target:
                    target[key] = value
                else:
                    target[key] = self.merge_extends(
                        target[key], value, inherit_key, inherit)
        elif isinstance(target, list) and isinstance(extends, list):
            if inherit:
                target.extend(extends)
            else:
                target = extends
        else:
            target = extends
        return target

    def merge_sources(self, datas):
        """Merge multiple data sources into one."""
        result = {}
        for data in datas:
            result = self.merge_extends(result, data)
        return result

    def merge_configs(self, config, datas):
        """Merge config with data sources."""
        result = self.merge_sources(datas)
        return self.merge_extends(result, config)
