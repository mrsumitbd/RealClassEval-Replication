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
        self.sql_type = sql_type
        self.primary_key = primary_key
        self.nullable = nullable
        self.default = default

    def ddl(self) -> str:
        '''
        Generate the SQL DDL statement for this field.
        '''
        ddl_parts = [self.sql_type]
        if self.primary_key:
            ddl_parts.append("PRIMARY KEY")
        if not self.nullable:
            ddl_parts.append("NOT NULL")
        if self.default is not None:
            if isinstance(self.default, str):
                default_val = f"'{self.default}'"
            elif isinstance(self.default, bool):
                default_val = '1' if self.default else '0'
            else:
                default_val = str(self.default)
            ddl_parts.append(f"DEFAULT {default_val}")
        return " ".join(ddl_parts)
