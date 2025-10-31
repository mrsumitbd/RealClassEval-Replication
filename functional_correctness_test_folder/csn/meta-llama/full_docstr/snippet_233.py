
from typing import Dict


class TemplateVersion:
    def __init__(self, name: str, timestamp: int):
        self.name = name
        self.timestamp = timestamp


class Template:
    '''
    Disk image template class
    Attributes:
        name (str): Name of this template
        _versions (dict(str:TemplateVersion)): versions for this template
    '''

    def __init__(self, name: str, versions: Dict[str, 'TemplateVersion']):
        '''
        Args:
            name (str): Name of the template
            versions (dict(str:TemplateVersion)): dictionary with the
                version_name: :class:`TemplateVersion` pairs for this template
        '''
        self.name = name
        self._versions = versions

    def get_version(self, ver_name: str = None) -> 'TemplateVersion':
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

    def get_latest_version(self) -> 'TemplateVersion':
        '''
        Retrieves the latest version for this template, the latest being the
        one with the newest timestamp
        Returns:
            TemplateVersion
        '''
        if not self._versions:
            return None
        return max(self._versions.values(), key=lambda x: x.timestamp)


# Example usage:
if __name__ == "__main__":
    v1 = TemplateVersion('v1', 1643723400)
    v2 = TemplateVersion('v2', 1643723410)
    v3 = TemplateVersion('v3', 1643723420)

    template = Template('my_template', {'v1': v1, 'v2': v2, 'v3': v3})

    print(template.get_version('v2').name)  # Output: v2
    print(template.get_latest_version().name)  # Output: v3
    print(template.get_version().name)  # Output: v3
