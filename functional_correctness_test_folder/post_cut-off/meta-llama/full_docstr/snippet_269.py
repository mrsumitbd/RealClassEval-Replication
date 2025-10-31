
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
        ddl = f'{self.sql_type}'
        if self.primary_key:
            ddl += ' PRIMARY KEY'
        if not self.nullable:
            ddl += ' NOT NULL'
        if self.default is not None:
            if isinstance(self.default, str):
                ddl += f" DEFAULT '{self.default}'"
            else:
                ddl += f' DEFAULT {self.default}'
        return ddl


# Example usage:
if __name__ == "__main__":
    field1 = Field('INT', primary_key=True)
    print(field1.ddl())  # Output: INT PRIMARY KEY

    field2 = Field('VARCHAR(255)', nullable=False, default='Unknown')
    print(field2.ddl())  # Output: VARCHAR(255) NOT NULL DEFAULT 'Unknown'

    field3 = Field('BOOLEAN', default=True)
    print(field3.ddl())  # Output: BOOLEAN DEFAULT True
