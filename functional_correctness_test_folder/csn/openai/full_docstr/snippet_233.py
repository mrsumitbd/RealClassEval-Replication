
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
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not isinstance(versions, dict):
            raise TypeError("versions must be a dict")
        for k, v in versions.items():
            if not isinstance(k, str):
                raise TypeError("version keys must be strings")
            if not hasattr(v, "__dict__"):
                raise TypeError("version values must be objects")
        self.name = name
        self._versions = dict(versions)

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
        try:
            return self._versions[ver_name]
        except KeyError:
            raise KeyError(
                f"Version '{ver_name}' not found in template '{self.name}'")

    def get_latest_version(self):
        '''
        Retrieves the latest version for this template, the latest being the
        one with the newest timestamp
        Returns:
            TemplateVersion
        '''
        if not self._versions:
            raise ValueError(
                f"No versions available for template '{self.name}'")
        # Assume each TemplateVersion has a 'timestamp' attribute that is
        # comparable (e.g., datetime or numeric). If not present, fall back
        # to the order of insertion.

        def _timestamp(v):
            return getattr(v, "timestamp", None)

        # If all timestamps are None, use insertion order
        if all(_timestamp(v) is None for v in self._versions.values()):
            # Python 3.7+ preserves dict order
            return next(reversed(self._versions.values()))
        return max(self._versions.values(), key=_timestamp)
