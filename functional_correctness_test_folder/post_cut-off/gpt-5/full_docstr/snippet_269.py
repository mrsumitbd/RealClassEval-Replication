from typing import Any
from datetime import date, datetime, time


class Field:
    '''
    Class representing a database field.
    '''

    def __init__(self, sql_type: str, primary_key: bool = False, nullable: bool = True, default: Any = None):
        '''
        Initialize a new Field instance.
        sql_type -- The SQL data type of the field.
        primary_key -- Whether this field is a primary key.
        nullable -- Whether this field can be null.
        default -- The default value for this field.
        '''
        if not isinstance(sql_type, str) or not sql_type.strip():
            raise ValueError("sql_type must be a non-empty string")
        self.sql_type = sql_type.strip()
        self.primary_key = bool(primary_key)
        self.nullable = bool(nullable)
        self.default = default

    def _format_default(self, value: Any) -> str:
        if value is None:
            raise ValueError("Default value is None; should not be formatted.")
        if isinstance(value, bool):
            return "TRUE" if value else "FALSE"
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, (date, datetime, time)):
            return f"'{value.isoformat()}'"
        if isinstance(value, bytes):
            return f"X'{value.hex()}'"
        if isinstance(value, str):
            escaped = value.replace("'", "''")
            return f"'{escaped}'"
        raise TypeError(f"Unsupported default type: {type(value).__name__}")

    def ddl(self) -> str:
        parts = [self.sql_type]

        if self.primary_key or not self.nullable:
            parts.append("NOT NULL")
        else:
            parts.append("NULL")

        if self.default is not None:
            parts.append(f"DEFAULT {self._format_default(self.default)}")

        if self.primary_key:
            parts.append("PRIMARY KEY")

        return " ".join(parts)
