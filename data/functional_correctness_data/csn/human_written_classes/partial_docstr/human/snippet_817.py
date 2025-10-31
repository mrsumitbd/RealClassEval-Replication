class DependencySection:
    """Group of dependencies that are displayed together in ``imount --check``.

    :param str name: name for the group
    :param str description: explanation of which dependencies in the group are needed.
    :param list[Dependency] deps: dependencies that are part of this group.
    """

    def __init__(self, name, description, deps):
        self.name = name
        self.description = description
        self.deps = deps

    @property
    def printable_status(self):
        lines = ['-- {0.name} ({0.description}) --'.format(self)]
        for dep in self.deps:
            lines.append(' ' + dep.printable_status)
        return '\n'.join(lines)