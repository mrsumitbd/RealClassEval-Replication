
from typing import Any


class Field:
    """
    Class representing a database field.
    """

    def __init__(self, sql_type: str, primary_key: bool = False,
                 nullable: bool = True, default: Any = None):
        """
        Initialize a new Field instance.

        :param sql_type: The SQL data type of the field.
        :param primary_key: Whether this field is a primary key.
        :param nullable: Whether this field can be null.
        :param default: The default value for this field.
        """
        self.sql_type = sql_type
        self.primary_key = primary_key
        self.nullable = nullable
        self.default = default

    def ddl(self) -> str:
        """
        Generate the SQL DDL statement for this field.
        """
        parts = [self.sql_type]

        if self.primary_key:
            parts.append("PRIMARY KEY")

        if not self.nullable:
            parts.append("NOT NULL")

        if self.default is not None:
            # Use repr to get a valid SQL literal for most Python types.
            # For strings, repr adds quotes; for numbers and booleans it works as well.
            parts.append(f"DEFAULT {repr(self.default)}")

        return " ".join(parts)
