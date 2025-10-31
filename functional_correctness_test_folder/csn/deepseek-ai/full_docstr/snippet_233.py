
class Template:
    '''
    Disk image template class
    Attributes:
        name (str): Name of this template
        _versions (dict(str:TemplateVersion)): versions for this template
    '''

    def __init__(self, name, versions):
        '''
        Args:
            name (str): Name of the template
            versions (dict(str:TemplateVersion)): dictionary with the
                version_name: :class:`TemplateVersion` pairs for this template
        '''
        self.name = name
        self._versions = versions

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
        return self._versions.get(ver_name)

    def get_latest_version(self):
        '''
        Retrieves the latest version for this template, the latest being the
        one with the newest timestamp
        Returns:
            TemplateVersion
        '''
        if not self._versions:
            return None
        return max(self._versions.values(), key=lambda v: v.timestamp)
