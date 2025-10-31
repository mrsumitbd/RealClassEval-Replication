
from typing import Any


class Field:
    """
    Class representing a database field.
    """

    def __init__(self, sql_type: str, primary_key: bool = False, nullable: bool = True, default: Any = None):
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

    def _format_default(self) -> str:
        """Return the SQL representation of the default value."""
        if self.default is None:
            return "NULL"
        if isinstance(self.default, str):
            # Escape single quotes in the string
            escaped = self.default.replace("'", "''")
            return f"'{escaped}'"
        if isinstance(self.default, bool):
            return "TRUE" if self.default else "FALSE"
        # For numbers and other types, use str()
        return str(self.default)

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
            parts.append(f"DEFAULT {self._format_default()}")

        return " ".join(parts)
