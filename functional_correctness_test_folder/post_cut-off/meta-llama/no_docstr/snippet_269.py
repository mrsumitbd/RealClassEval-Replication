
from typing import Any


class Field:

    def __init__(self, sql_type: str, primary_key: bool = False, nullable: bool = True, default: Any = None):
        self.sql_type = sql_type
        self.primary_key = primary_key
        self.nullable = nullable
        self.default = default

    def ddl(self) -> str:
        ddl_str = self.sql_type
        if self.primary_key:
            ddl_str += ' PRIMARY KEY'
        if not self.nullable:
            ddl_str += ' NOT NULL'
        if self.default is not None:
            if isinstance(self.default, str):
                ddl_str += f" DEFAULT '{self.default}'"
            else:
                ddl_str += f' DEFAULT {self.default}'
        return ddl_str
