
from typing import Any


class Field:

    def __init__(self, sql_type: str, primary_key: bool = False, nullable: bool = True, default: Any = None):
        self.sql_type = sql_type
        self.primary_key = primary_key
        self.nullable = nullable
        self.default = default

    def ddl(self) -> str:
        parts = [self.sql_type]
        if self.primary_key:
            parts.append("PRIMARY KEY")
        if not self.nullable:
            parts.append("NOT NULL")
        if self.default is not None:
            if isinstance(self.default, str):
                default_val = f"'{self.default}'"
            elif isinstance(self.default, bool):
                default_val = '1' if self.default else '0'
            else:
                default_val = str(self.default)
            parts.append(f"DEFAULT {default_val}")
        return " ".join(parts)
