import fnmatch

class GlobMatch:

    def __init__(self, pattern: list[str]) -> None:
        self.pattern_list: list[str] = pattern

    def match(self, filename: str) -> bool:
        return any((fnmatch.fnmatch(filename, p) for p in self.pattern_list))