from typing import IO, Any


class FieldDefinition:
    PY_TO_DSL_TYPES = {
        "str": "xsd:string",
        "int": "xsd:int",
        "float": "xsd:float",
        "bool": "xsd:boolean",
        "bytes": "xsd:base64Binary",
        "datetime": "xsd:dateTime",
        "date": "xsd:date",
        "time": "xsd:time",
        "decimal": "xsd:decimal",
    }

    def __init__(self, name: str, typeStr: str, optional: bool, mapSubject: str, mapPredicate: str, typeDSL: bool):
        self.name = (name or "").strip()
        self.typeStr = (typeStr or "").strip()
        self.optional = bool(optional)
        self.mapSubject = (mapSubject or "").strip()
        self.mapPredicate = (mapPredicate or "").strip()
        self.typeDSL = bool(typeDSL)

        if not self.name:
            raise ValueError("Field name must be a non-empty string.")
        if not self.typeStr:
            raise ValueError("typeStr must be a non-empty string.")

    def _resolve_type(self) -> str:
        if self.typeDSL:
            return self.typeStr
        key = self.typeStr.strip()
        # normalize common annotations like "string", "boolean"
        normalized = {
            "string": "str",
            "integer": "int",
            "number": "float",
            "boolean": "bool",
        }.get(key.lower(), key)
        return self.PY_TO_DSL_TYPES.get(normalized, normalized)

    @staticmethod
    def _join_namespace(namespace: str, value: str) -> str:
        if not value:
            return value
        ns = (namespace or "").strip()
        v = value.strip()
        if not ns:
            return v
        # If value already looks namespaced or absolute, return as-is
        if ":" in v or v.startswith("http://") or v.startswith("https://"):
            return v
        # Ensure a separator if namespace does not end with one
        if ns.endswith(("/", "#", ":")):
            return f"{ns}{v}"
        return f"{ns}:{v}"

    def writeDefinition(self, target: IO[Any], fullInd: str, ind: str, namespace: str) -> None:
        if target is None:
            raise ValueError("target must be a writable IO.")
        base = fullInd or ""
        step = ind or ""

        resolved_type = self._resolve_type()
        opt_suffix = "?" if self.optional else ""

        # Field signature
        target.write(f"{base}{self.name}: {resolved_type}{opt_suffix}\n")

        # Mapping details
        if self.mapSubject:
            target.write(f"{base}{step}subject: {self.mapSubject}\n")
        if self.mapPredicate:
            predicate = self._join_namespace(namespace, self.mapPredicate)
            target.write(f"{base}{step}predicate: {predicate}\n")
