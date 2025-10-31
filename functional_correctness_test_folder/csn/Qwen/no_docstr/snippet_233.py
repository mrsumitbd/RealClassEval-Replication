
class Template:

    def __init__(self, name, versions):
        self.name = name
        self.versions = versions  # Assuming versions is a list of version strings

    def get_version(self, ver_name=None):
        if ver_name is None:
            return self.versions
        else:
            for version in self.versions:
                if version == ver_name:
                    return version
            return None

    def get_latest_version(self):
        if not self.versions:
            return None
        # Assuming versions are in the format 'x.y.z' and are sortable
        return sorted(self.versions, key=lambda v: [int(part) for part in v.split('.')])[-1]
