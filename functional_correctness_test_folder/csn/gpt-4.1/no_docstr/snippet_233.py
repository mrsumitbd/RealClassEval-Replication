
class Template:

    def __init__(self, name, versions):
        self.name = name
        # versions: list of dicts, each with 'name' and 'content'
        self.versions = versions

    def get_version(self, ver_name=None):
        if ver_name is None:
            return self.get_latest_version()
        for v in self.versions:
            if v.get('name') == ver_name:
                return v
        return None

    def get_latest_version(self):
        if not self.versions:
            return None
        return self.versions[-1]
