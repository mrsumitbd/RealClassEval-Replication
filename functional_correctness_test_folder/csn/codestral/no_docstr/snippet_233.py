
class Template:

    def __init__(self, name, versions):
        self.name = name
        self.versions = versions

    def get_version(self, ver_name=None):
        if ver_name is None:
            return self.versions
        return self.versions.get(ver_name)

    def get_latest_version(self):
        if not self.versions:
            return None
        latest_version = max(self.versions.keys())
        return self.versions[latest_version]
