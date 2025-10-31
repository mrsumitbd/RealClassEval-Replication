from typing import Iterator, List, Optional, Set, Tuple

class UcdFile:
    """
    A file in the standard format of the UCD.

    See: https://www.unicode.org/reports/tr44/#Format_Conventions

    Note that, as described there, the Unihan data files have their
    own separate format.
    """

    def __init__(self, template: str, version: str) -> None:
        self.template = template
        self.version = version

    def records(self) -> Iterator[List[str]]:
        with open_data(self.template, self.version) as file:
            for line in file:
                line = line.split('#', 1)[0].strip()
                if not line:
                    continue
                yield [field.strip() for field in line.split(';')]

    def __iter__(self) -> Iterator[List[str]]:
        return self.records()

    def expanded(self) -> Iterator[Tuple[int, List[str]]]:
        for record in self.records():
            char_range, rest = (record[0], record[1:])
            for char in expand_range(char_range):
                yield (char, rest)