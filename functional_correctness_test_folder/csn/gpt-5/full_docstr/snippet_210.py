from typing import IO, List
import keyword
import re


class EnumDefinition:
    '''Prototype of a enum.'''

    def __init__(self, name: str, values: List[str]):
        '''Initialize enum definition with a name and possible values.'''
        if not isinstance(name, str) or not name:
            raise ValueError("Enum name must be a non-empty string")
        if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
            raise ValueError("Enum values must be a list of strings")
        self.name = name
        self.values = values[:]

    def _sanitize_member(self, value: str) -> str:
        s = re.sub(r'\W+', '_', value).strip('_')
        if not s:
            s = "VALUE"
        if s[0].isdigit():
            s = f"_{s}"
        s = s.upper()
        if keyword.iskeyword(s):
            s = f"{s}_"
        return s

    def writeDefinition(self, target: IO[str], ind: str, common_namespace: str) -> None:
        '''Write enum definition to output.'''
        # optional comment with namespace info
        if common_namespace:
            target.write(f"{ind}# namespace: {common_namespace}\n")
        target.write(f"{ind}class {self.name}(Enum):\n")
        if not self.values:
            target.write(f"{ind}{ind}pass\n")
            return
        used = {}
        for i, val in enumerate(self.values):
            member = self._sanitize_member(val)
            base = member
            suffix = 1
            while member in used:
                suffix += 1
                member = f"{base}_{suffix}"
            used[member] = True
            target.write(f"{ind}{ind}{member} = {val!r}\n")
