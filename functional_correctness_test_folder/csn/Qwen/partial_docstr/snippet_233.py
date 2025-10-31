
class TemplateVersion:
    def __init__(self, name, content):
        self.name = name
        self.content = content


class Template:

    def __init__(self, name, versions):
        self.name = name
        self.versions = versions  # Assuming versions is a list of TemplateVersion objects

    def get_version(self, ver_name=None):
        if ver_name:
            for version in self.versions:
                if version.name == ver_name:
                    return version
        return self.get_latest_version()

    def get_latest_version(self):
        if self.versions:
            return max(self.versions, key=lambda v: v.name)
        return None
