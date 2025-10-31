
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
        ddl = self.sql_type
        if self.primary_key:
            ddl += " PRIMARY KEY"
        if not self.nullable:
            ddl += " NOT NULL"
        if self.default is not None:
            ddl += f" DEFAULT {self.default}"
        return ddl
