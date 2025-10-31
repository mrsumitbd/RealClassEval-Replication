
class Template:
    def __init__(self, name, versions):
        """
        Initialize a Template instance.

        Args:
            name (str): The name of the template.
            versions (list): A list of version objects. Each object must have a
                `name` attribute that represents the version string.
        """
        self.name = name
        # Ensure versions is a list
        self.versions = list(versions)

        # Sort versions by parsed version number for consistent ordering
        self.versions.sort(key=lambda v: self._parse_version(v.name))

    def get_version(self, ver_name=None):
        """
        Get the given version for this template, or the latest.

        Args:
            ver_name (str or None): Version to retrieve, None for the latest.

        Returns:
            The version object matching the given name or the latest one.

        Raises:
            ValueError: If the requested version is not found.
        """
        if ver_name is None:
            return self.get_latest_version()

        for v in self.versions:
            if v.name == ver_name:
                return v

        raise ValueError(
            f"Version '{ver_name}' not found in template '{self.name}'")

    def get_latest_version(self):
        """
        Return the latest version of the template.

        Returns:
            The latest version object.

        Raises:
            ValueError: If there are no versions available.
        """
        if not self.versions:
            raise ValueError(
                f"No versions available for template '{self.name}'")
        return self.versions[-1]

    @staticmethod
    def _parse_version(ver_str):
        """
        Parse a version string into a tuple of integers for comparison.

        Examples:
            "1.2.3" -> (1, 2, 3)
            "2.0"   -> (2, 0)
            "10"    -> (10,)

        Args:
            ver_str (str): The version string.

        Returns:
            tuple[int]: Parsed version components.
        """
        parts = ver_str.split('.')
        nums = []
        for part in parts:
            try:
                nums.append(int(part))
            except ValueError:
                # Non-numeric part: treat as 0 for comparison
                nums.append(0)
        return tuple(nums)
