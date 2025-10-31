
class TemplateVersion:
    def __init__(self, name, version):
        self.name = name
        self.version = version

    def __repr__(self):
        return f'TemplateVersion(name={self.name}, version={self.version})'


class Template:

    def __init__(self, name, versions):
        """
        Initialize a Template object.

        Args:
            name (str): The name of the template.
            versions (list of TemplateVersion): A list of TemplateVersion objects.
        """
        self.name = name
        self.versions = {version.version: version for version in versions}
        self.versions_list = sorted(list(self.versions.keys()), reverse=True)

    def get_version(self, ver_name=None):
        '''
        Get the given version for this template, or the latest

        Args:
            ver_name (str or None): Version to retieve, None for the latest

        Returns:
            TemplateVersion: The version matching the given name or the latest one
        '''
        if ver_name is None:
            return self.get_latest_version()
        return self.versions.get(ver_name)

    def get_latest_version(self):
        """
        Get the latest version of the template.

        Returns:
            TemplateVersion: The latest TemplateVersion object.
        """
        if not self.versions_list:
            return None
        return self.versions[self.versions_list[0]]


# Example usage:
if __name__ == "__main__":
    v1 = TemplateVersion('template1', '1.0')
    v2 = TemplateVersion('template1', '2.0')
    v3 = TemplateVersion('template1', '3.0')

    template = Template('template1', [v1, v2, v3])

    # TemplateVersion(name=template1, version=2.0)
    print(template.get_version('2.0'))
    # TemplateVersion(name=template1, version=3.0)
    print(template.get_latest_version())
    # TemplateVersion(name=template1, version=3.0)
    print(template.get_version())
