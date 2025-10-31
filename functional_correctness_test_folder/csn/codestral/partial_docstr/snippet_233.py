
class Template:

    def __init__(self, name, versions):
        self.name = name
        self.versions = versions

    def get_version(self, ver_name=None):
        if ver_name is None:
            return self.get_latest_version()
        for version in self.versions:
            if version.name == ver_name:
                return version
        raise ValueError(f"Version {ver_name} not found")

    def get_latest_version(self):
        if not self.versions:
            raise ValueError("No versions available")
        return max(self.versions, key=lambda v: v.version_number)
