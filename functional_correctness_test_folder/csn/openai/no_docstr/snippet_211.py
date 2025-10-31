
from typing import IO, Any


class FieldDefinition:
    """
    Represents a field definition in a DSL or schema generator.

    Attributes
    ----------
    name : str
        The name of the field.
    typeStr : str
        The type of the field as a string.
    optional : bool
        Whether the field is optional.
    mapSubject : str
        Mapping subject string (used in RDF or similar contexts).
    mapPredicate : str
        Mapping predicate string.
    typeDSL : bool
        Flag indicating if the type is a DSL type.
    """

    def __init__(
        self,
        name: str,
        typeStr: str,
        optional: bool,
        mapSubject: str,
        mapPredicate: str,
        typeDSL: bool,
    ):
        self.name = name
        self.typeStr = typeStr
        self.optional = optional
        self.mapSubject = mapSubject
        self.mapPredicate = mapPredicate
        self.typeDSL = typeDSL

    def writeDefinition(self, target: IO[Any], fullInd: str, ind: str, namespace: str) -> None:
        """
        Write the field definition to the given target stream.

        Parameters
        ----------
        target : IO[Any]
            The output stream to write to.
        fullInd : str
            The indentation string for the top-level line.
        ind : str
            The indentation string for nested lines.
        namespace : str
            Namespace to prepend to the type if it is not already fully qualified.
        """
        # Resolve the type string with namespace if needed
        if namespace and not self.typeStr.startswith(namespace):
            type_str = f"{namespace}.{self.typeStr}"
        else:
            type_str = self.typeStr

        # Optional marker
        opt_marker = "?" if self.optional else ""

        # Write the main field line
        target.write(f"{fullInd}field {self.name}{opt_marker}: {type_str}\n")

        # Write additional metadata lines
        target.write(f"{fullInd}{ind}mapSubject: {self.mapSubject}\n")
        target.write(f"{fullInd}{ind}mapPredicate: {self.mapPredicate}\n")
        target.write(f"{fullInd}{ind}typeDSL: {self.typeDSL}\n")
