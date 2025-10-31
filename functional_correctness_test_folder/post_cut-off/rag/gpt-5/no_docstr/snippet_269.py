from typing import Any


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
        if not sql_type or not isinstance(sql_type, str):
            raise ValueError("sql_type must be a non-empty string")
        self.sql_type = sql_type.strip()
        self.primary_key = bool(primary_key)
        # Primary keys are implicitly NOT NULL in most SQL dialects
        self.nullable = False if self.primary_key else bool(nullable)
        self.default = default

    def ddl(self) -> str:
        '''
        Generate the SQL DDL statement for this field.
        '''
        parts: list[str] = [self.sql_type]
        if self.primary_key:
            parts.append('PRIMARY KEY')
        if not self.nullable:
            parts.append('NOT NULL')
        if self.default is not None:
            def _format_default(value: Any) -> str:
                if isinstance(value, bool):
                    return 'TRUE' if value else 'FALSE'
                if isinstance(value, (int, float)):
                    return str(value)
                if isinstance(value, str):
                    escaped = value.replace("'", "''")
                    return f"'{escaped}'"
                # Fallback: stringify and quote
                escaped = str(value).replace("'", "''")
                return f"'{escaped}'"
            parts.append(f'DEFAULT {_format_default(self.default)}')
        return ' '.join(parts)
