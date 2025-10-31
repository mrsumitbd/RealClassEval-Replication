from typing import Any
import re


class Field:

    def __init__(self, sql_type: str, primary_key: bool = False, nullable: bool = True, default: Any = None):
        if not isinstance(sql_type, str) or not sql_type.strip():
            raise ValueError("sql_type must be a non-empty string")
        self.sql_type = sql_type.strip()
        self.primary_key = bool(primary_key)
        self.nullable = False if self.primary_key else bool(nullable)
        self.default = default

    def _format_default(self, value: Any) -> str | None:
        if value is None:
            return None
        if isinstance(value, bool):
            return 'TRUE' if value else 'FALSE'
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, str):
            # Treat uppercase identifiers/functions as raw tokens (e.g., CURRENT_TIMESTAMP, NOW())
            if re.fullmatch(r'[A-Z_][A-Z0-9_]*(\(\))?', value):
                return value
            vq = value.replace("'", "''")
            return f"'{vq}'"
        try:
            s = str(value).replace("'", "''")
            return f"'{s}'"
        except Exception:
            return None

    def ddl(self) -> str:
        parts = [self.sql_type]
        if self.primary_key:
            parts.append('PRIMARY KEY')
        parts.append('NOT NULL' if not self.nullable else 'NULL')
        d = self._format_default(self.default)
        if d is not None:
            parts.append(f'DEFAULT {d}')
        return ' '.join(parts)
