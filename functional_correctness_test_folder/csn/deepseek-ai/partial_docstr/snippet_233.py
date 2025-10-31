
class Template:

    def __init__(self, name, versions):
        self.name = name
        self.versions = versions

    def get_version(self, ver_name=None):
        '''
        Get the given version for this template, or the latest
        Args:
            ver_name (str or None): Version to retieve, None for the latest
        Returns:
            TemplateVersion: The version matching the given name or the latest
                one
        '''
        if ver_name is None:
            return self.get_latest_version()
        for version in self.versions:
            if version.name == ver_name:
                return version
        return None

    def get_latest_version(self):
        if not self.versions:
            return None
        return max(self.versions, key=lambda v: v.created_at)
