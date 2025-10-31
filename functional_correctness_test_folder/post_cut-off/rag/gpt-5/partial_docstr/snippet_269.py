from typing import Any


class Field:
    """
    Class representing a database field.
    """

    def __init__(self, sql_type: str, primary_key: bool = False, nullable: bool = True, default: Any = None):
        """
        Initialize a new Field instance.
        sql_type -- The SQL data type of the field.
        primary_key -- Whether this field is a primary key.
        nullable -- Whether this field can be null.
        default -- The default value for this field.
        """
        self.sql_type = sql_type
        self.primary_key = primary_key
        self.nullable = nullable
        self.default = default

    def _format_default(self, value: Any) -> str:
        if hasattr(value, "to_sql") and callable(getattr(value, "to_sql")):
            return str(value.to_sql())
        if hasattr(value, "as_sql") and callable(getattr(value, "as_sql")):
            return str(value.as_sql())

        if isinstance(value, bool):
            return "TRUE" if value else "FALSE"
        if isinstance(value, (int, float)):
            return str(value)
        if value is None:
            return "NULL"
        # Fallback to string literal with single-quote escaping
        text = str(value).replace("'", "''")
        return f"'{text}'"

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
            parts.append(f"DEFAULT {self._format_default(self.default)}")

        return " ".join(parts)
