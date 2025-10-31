from collections.abc import Iterator

class SourceContents:
    """Used to record the names of blueprints, bugs, and tools that are provided
    by a source.
    """

    def __init__(self, blueprints: list[str], bugs: list[str], tools: list[str]) -> None:
        self.__blueprints = blueprints[:]
        self.__bugs = bugs[:]
        self.__tools = tools[:]

    @property
    def blueprints(self) -> Iterator[str]:
        """The names of the blueprints that are provided by the source.
        """
        return self.__blueprints.__iter__()

    @property
    def bugs(self) -> Iterator[str]:
        """The names of the bugs that are provided by the source.
        """
        return self.__bugs.__iter__()

    @property
    def tools(self) -> Iterator[str]:
        """The names of the tools that are provided by the source.
        """
        return self.__tools.__iter__()