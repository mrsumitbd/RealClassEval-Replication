
class Template:

    def __init__(self, name, versions):
        """
        Initialize a Template object.

        Args:
            name (str): The name of the template.
            versions (dict): A dictionary where keys are version names and values are version details.
        """
        self.name = name
        self.versions = versions

    def get_version(self, ver_name=None):
        """
        Get a specific version of the template.

        Args:
            ver_name (str, optional): The name of the version to retrieve. Defaults to None.

        Returns:
            The version details if ver_name is provided, otherwise returns all versions.
        """
        if ver_name is None:
            return self.versions
        return self.versions.get(ver_name)

    def get_latest_version(self):
        """
        Get the latest version of the template.

        Returns:
            The latest version details.
        """
        if not self.versions:
            return None
        return max(self.versions.items(), key=lambda x: x[0])[1]


# Example usage:
if __name__ == "__main__":
    template = Template("example_template", {
        "v1": "Version 1 details",
        "v2": "Version 2 details",
        "v3": "Version 3 details"
    })

    print(template.get_version("v2"))  # Output: Version 2 details
    # Output: {'v1': 'Version 1 details', 'v2': 'Version 2 details', 'v3': 'Version 3 details'}
    print(template.get_version())
    print(template.get_latest_version())  # Output: Version 3 details
