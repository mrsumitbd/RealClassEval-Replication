
from typing import Any


class Field:
    def __init__(self, sql_type: str, primary_key: bool = False, nullable: bool = True, default: Any = None):
        self.sql_type = sql_type
        self.primary_key = primary_key
        self.nullable = nullable
        self.default = default

    def _format_default(self) -> str:
        if self.default is None:
            return ""
        # Booleans
        if isinstance(self.default, bool):
            return str(int(self.default))
        # Numbers
        if isinstance(self.default, (int, float)):
            return str(self.default)
        # Strings
        if isinstance(self.default, str):
            # Escape single quotes
            escaped = self.default.replace("'", "''")
            return f"'{escaped}'"
        # Other types: use str representation
        return str(self.default)

    def ddl(self) -> str:
        parts = [self.sql_type]
        if self.primary_key:
            parts.append("PRIMARY KEY")
        if not self.nullable or self.primary_key:
            parts.append("NOT NULL")
        default_sql = self._format_default()
        if default_sql:
            parts.append(f"DEFAULT {default_sql}")
        return " ".join(parts)
