class ArtifactoryBuild:
    __slots__ = ('name', 'last_started', 'build_manager')

    def __init__(self, name, last_started, build_manager):
        self.name = name
        self.last_started = last_started
        self.build_manager = build_manager

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @property
    def runs(self):
        """
        Get information about build runs
        :return: List[ArtifactoryBuildRun]
        """
        return self.build_manager.get_build_runs(self.name)