class Source:
    """Sources are used to provide access to blueprints for constructing bugs
    and tools. Sources can be provided by either local directories or remote
    Git repositories.
    """

    @staticmethod
    def from_dict(d: dict) -> 'Source':
        if d['type'] == 'local':
            return LocalSource.from_dict(d)
        if d['type'] == 'remote':
            return RemoteSource.from_dict(d)
        raise Exception('unsupported source type: {}'.format(d['type']))

    def __init__(self, name: str, location: str) -> None:
        self.__location = location
        self.__name = name

    @property
    def name(self) -> str:
        """The name of this source.
        """
        return self.__name

    @property
    def location(self) -> str:
        """The location of this source on disk.
        """
        return self.__location