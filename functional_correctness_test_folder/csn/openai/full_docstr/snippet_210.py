
from typing import IO, List


class EnumDefinition:
    '''Prototype of a enum.'''

    def __init__(self, name: str, values: List[str]):
        '''Initialize enum definition with a name and possible values.'''
        self.name = name
        self.values = values

    def writeDefinition(self, target: IO[str], ind: str, common_namespace: str) -> None:
        '''Write enum definition to output.'''
        # Helper to write a line with the current indentation
        def write_line(line: str = ""):
            target.write(f"{ind}{line}\n")

        # If a namespace is provided, open it
        if common_namespace:
            write_line(f"namespace {common_namespace} {{")
            # Increase indentation for the namespace body
            inner_ind = ind + "    "

            def write_inner(line: str = ""):
                target.write(f"{inner_ind}{line}\n")
            write_inner(f"enum {self.name} {{")
            for value in self.values:
                write_inner(f"{value},")
            write_inner("};")
            write_line("}")
        else:
            write_line(f"enum {self.name} {{")
            for value in self.values:
                write_line(f"    {value},")
            write_line("};")
