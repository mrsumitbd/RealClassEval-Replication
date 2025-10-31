
from typing import Any


class Field:

    def __init__(self, sql_type: str, primary_key: bool = False, nullable: bool = True, default: Any = None):
        self.sql_type = sql_type
        self.primary_key = primary_key
        self.nullable = nullable
        self.default = default

    def ddl(self) -> str:
        ddl_parts = [self.sql_type]
        if not self.nullable:
            ddl_parts.append("NOT NULL")
        if self.primary_key:
            ddl_parts.append("PRIMARY KEY")
        if self.default is not None:
            ddl_parts.append(f"DEFAULT {self.default}")
        return " ".join(ddl_parts)
