
from typing import IO, List


class EnumDefinition:
    """
    Represents an enumeration definition that can be written to a target stream.
    """

    def __init__(self, name: str, values: List[str]):
        """
        Initialize the enum definition.

        :param name: The name of the enum.
        :param values: A list of enum member names.
        """
        self.name = name
        self.values = values

    def _sanitize(self, value: str) -> str:
        """
        Sanitize a value to be a valid identifier: replace spaces and hyphens with underscores,
        remove leading digits, and strip invalid characters.

        :param value: The raw enum member name.
        :return: A sanitized identifier.
        """
        import re

        # Replace spaces and hyphens with underscores
        sanitized = re.sub(r"[ \-]+", "_", value)

        # Remove any character that is not a letter, digit, or underscore
        sanitized = re.sub(r"[^\w]", "", sanitized)

        # If it starts with a digit, prefix with an underscore
        if re.match(r"^\d", sanitized):
            sanitized = "_" + sanitized

        return sanitized

    def writeDefinition(self, target: IO[str], ind: str, common_namespace: str) -> None:
        """
        Write the enum definition to the target stream.

        The output format is a C++-style enum wrapped in a namespace if provided.

        Example output:

            namespace MyNamespace {
                enum MyEnum {
                    VALUE_ONE,
                    VALUE_TWO
                };
            }

        :param target: The stream to write to.
        :param ind: The indentation string to use for each level.
        :param common_namespace: The namespace to wrap the enum in; if empty, no namespace is used.
        """
        # Write namespace opening if needed
        if common_namespace:
            target.write(f"{ind}namespace {common_namespace} {{\n")
            namespace_ind = ind + ind  # increase indentation for namespace contents
        else:
            namespace_ind = ind

        # Write enum declaration
        target.write(f"{namespace_ind}enum {self.name} {{\n")

        # Write enum values
        for idx, raw_value in enumerate(self.values):
            value = self._sanitize(raw_value)
            comma = "," if idx < len(self.values) - 1 else ""
            target.write(f"{namespace_ind}{ind}{value}{comma}\n")

        # Close enum
        target.write(f"{namespace_ind}}};\n")

        # Close namespace if opened
        if common_namespace:
            target.write(f"{ind}}}\n")
