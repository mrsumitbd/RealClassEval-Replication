from typing import Any
from datetime import date, datetime, time
from decimal import Decimal


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
        # Primary keys are implicitly NOT NULL
        self.nullable = False if self.primary_key else bool(nullable)
        self.default = default

    def _sql_literal(self, value: Any) -> str:
        if value is None:
            return "NULL"
        if isinstance(value, bool):
            return "TRUE" if value else "FALSE"
        if isinstance(value, (int,)):
            return str(value)
        if isinstance(value, float):
            if value == float("inf"):
                return "'inf'"
            if value == float("-inf"):
                return "'-inf'"
            if value != value:  # NaN
                return "'nan'"
            return repr(value)
        if isinstance(value, Decimal):
            return format(value, 'f')
        if isinstance(value, (datetime, date, time)):
            return f"'{value.isoformat()}'"
        if isinstance(value, bytes):
            return "X'" + value.hex() + "'"
        # Fallback to string with SQL single-quote escaping
        s = str(value)
        s = s.replace("'", "''")
        return f"'{s}'"

    def ddl(self) -> str:
        '''
        Generate the SQL DDL statement for this field.
        '''
        parts = [self.sql_type]
        if self.primary_key:
            parts.append("PRIMARY KEY")
        parts.append("NOT NULL" if not self.nullable else "")
        # Only emit DEFAULT when a non-None default is provided
        if self.default is not None:
            parts.append(f"DEFAULT {self._sql_literal(self.default)}")
        # Clean empty segments and join
        return " ".join(p for p in parts if p)
