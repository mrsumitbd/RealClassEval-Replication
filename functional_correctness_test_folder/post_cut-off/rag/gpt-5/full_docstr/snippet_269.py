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
        # Primary key columns are implicitly NOT NULL in most SQL dialects
        self.nullable = False if self.primary_key else bool(nullable)
        self.default = default

    def _format_default(self, value: Any) -> str:
        if value is None:
            return 'NULL'
        if isinstance(value, bool):
            return 'TRUE' if value else 'FALSE'
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, (datetime, date, time)):
            # Use ISO8601 string for temporal values
            return f"'{value.isoformat()}'"
        if isinstance(value, bytes):
            # Render as hex literal (common across several SQL dialects)
            return f"X'{value.hex()}'"
        # Fallback to string literal with single-quote escaping
        s = str(value)
        s = s.replace("'", "''")
        return f"'{s}'"

    def ddl(self) -> str:
        '''
        Generate the SQL DDL statement for this field.
        '''
        parts: list[str] = [self.sql_type]
        # Constraints
        if self.primary_key:
            parts.append('PRIMARY KEY')
        if not self.nullable:
            parts.append('NOT NULL')
        # Default value
        if self.default is not None:
            parts.append('DEFAULT')
            parts.append(self._format_default(self.default))
        return ' '.join(parts)
