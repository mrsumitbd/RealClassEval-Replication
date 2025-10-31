class Template:
    def __init__(self, name, versions):
        """
        Initialize a Template instance.

        Parameters
        ----------
        name : str
            The name of the template.
        versions : list of tuples or dict
            A collection of versions. Each element can be a tuple
            (ver_name, ver_data) or a dict with keys 'name' and 'data'.
            The order of the collection determines the "latest" version.
        """
        self.name = name
        # Normalize versions to a list of (name, data) tuples
        self._versions = []
        for v in versions:
            if isinstance(v, dict):
                ver_name = v.get("name")
                ver_data = v.get("data")
            else:
                ver_name, ver_data = v
            if ver_name is None:
                raise ValueError("Each version must have a name")
            self._versions.append((ver_name, ver_data))

    def get_version(self, ver_name=None):
        """
        Retrieve a specific version by name, or the latest version if no name is provided.

        Parameters
        ----------
        ver_name : str, optional
            The name of the desired version. If omitted, the latest version is returned.

        Returns
        -------
        The data associated with the requested version.

        Raises
        ------
        KeyError
            If the requested version name does not exist.
        """
        if ver_name is None:
            return self.get_latest_version()
        for name, data in self._versions:
            if name == ver_name:
                return data
        raise KeyError(
            f"Version '{ver_name}' not found in template '{self.name}'")

    def get_latest_version(self):
        """
        Retrieve the most recently added version.

        Returns
        -------
        The data of the latest version.

        Raises
        ------
        IndexError
            If no versions are available.
        """
        if not self._versions:
            raise IndexError(
                f"No versions available for template '{self.name}'")
        return self._versions[-1][1]
