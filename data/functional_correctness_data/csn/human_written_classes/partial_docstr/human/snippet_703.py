from packaging.version import Version

class NameVerDependency:
    """A dependency indicated by name and version."""

    def __init__(self, name, version):
        self.name = name
        self.version = Version(version)

    def __eq__(self, other):
        return self.name == other.name and self.version == other.version

    def __hash__(self):
        return hash((self.name, self.version))

    def __lt__(self, other):
        assert not isinstance(self.version, str)
        return (self.name, self.version) < (other.name, other.version)