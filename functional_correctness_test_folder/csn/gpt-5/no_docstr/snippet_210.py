from typing import IO
import re


class EnumDefinition:
    def __init__(self, name: str, values: list[str]):
        if not isinstance(name, str) or not name:
            raise ValueError("Enum name must be a non-empty string")
        self.name = self._sanitize_identifier(
            name, allow_leading_underscore=False)
        if not self.name:
            raise ValueError("Enum name is invalid after sanitization")

        if not isinstance(values, list) or not values:
            raise ValueError("Enum values must be a non-empty list of strings")

        cleaned_values = []
        for v in values:
            if not isinstance(v, str) or not v:
                raise ValueError("Enum values must be non-empty strings")
            cv = self._sanitize_identifier(v, allow_leading_underscore=True)
            if not cv:
                raise ValueError(
                    f"Enum value '{v}' is invalid after sanitization")
            cleaned_values.append(cv)

        # Ensure uniqueness after sanitization
        seen = set()
        dedup = []
        for cv in cleaned_values:
            if cv in seen:
                raise ValueError(f"Duplicate enum value detected: {cv}")
            seen.add(cv)
            dedup.append(cv)

        self.values = dedup

    def writeDefinition(self, target: IO[str], ind: str, common_namespace: str) -> None:
        if ind is None:
            ind = ""

        # Prepare namespaces
        ns_segments = self._split_namespaces(
            common_namespace) if common_namespace else []

        current_indent = ""
        # Open namespaces
        for seg in ns_segments:
            target.write(f"{current_indent}namespace {seg} {{\n")
            current_indent += ind

        # Write enum
        target.write(f"{current_indent}enum class {self.name} {{\n")
        inner_indent = current_indent + ind

        for i, val in enumerate(self.values):
            comma = "," if i < len(self.values) - 1 else ""
            target.write(f"{inner_indent}{val}{comma}\n")

        target.write(f"{current_indent}}};\n")

        # Close namespaces
        for seg in reversed(ns_segments):
            current_indent = current_indent[:-
                                            len(ind)] if len(ind) <= len(current_indent) else ""
            target.write(f"{current_indent}}} // namespace {seg}\n")

    @staticmethod
    def _sanitize_identifier(s: str, allow_leading_underscore: bool) -> str:
        # Replace invalid characters with underscore
        s = re.sub(r"\W", "_", s)
        # Remove leading digits
        if s and s[0].isdigit():
            s = "_" + s
        # Disallow empty result
        if not s:
            return s
        # For enum name, avoid leading underscore if not allowed
        if not allow_leading_underscore and s.startswith("_"):
            s = "E" + s
        return s

    @staticmethod
    def _split_namespaces(ns: str) -> list[str]:
        if not ns:
            return []
        # Support 'A::B::C' and 'A.B.C'
        parts = []
        for chunk in ns.split("::"):
            parts.extend(chunk.split("."))
        # Sanitize each namespace segment
        clean = []
        for p in parts:
            p = re.sub(r"\W", "_", p)
            if p and p[0].isdigit():
                p = "_" + p
            if p:
                clean.append(p)
        return [p for p in clean if p]
