class FieldDefinition:
    '''Prototype of a single field from a class definition.'''

    def __init__(self, name: str, typeStr: str, optional: bool, mapSubject: str, mapPredicate: str, typeDSL: bool):
        '''Initialize field definition.
        Creates a new field with name, its type, optional and which field to use to convert
        from list to map (or empty if it is not possible)
        '''
        self.name = name
        self.typeStr = typeStr
        self.optional = bool(optional)
        self.mapSubject = mapSubject or ""
        self.mapPredicate = mapPredicate or ""
        self.typeDSL = bool(typeDSL)

    def _is_qualified(self, t: str) -> bool:
        return "::" in t

    def _has_templates(self, t: str) -> bool:
        return "<" in t and ">" in t

    def _normalize_basic_type(self, t: str) -> str:
        basic_map = {
            "string": "std::string",
            "std::string": "std::string",
            "int": "int",
            "int32": "int32_t",
            "int32_t": "int32_t",
            "int64": "int64_t",
            "int64_t": "int64_t",
            "uint32": "uint32_t",
            "uint32_t": "uint32_t",
            "uint64": "uint64_t",
            "uint64_t": "uint64_t",
            "float": "float",
            "double": "double",
            "bool": "bool",
            "char": "char",
            "size_t": "size_t",
        }
        return basic_map.get(t, t)

    def _should_prefix_namespace(self, t: str) -> bool:
        # Do not prefix for known builtins or already qualified or template types
        builtins = {
            "std::string", "string", "int", "int32_t", "int64_t",
            "uint32_t", "uint64_t", "float", "double", "bool",
            "char", "size_t", "void",
        }
        if t in builtins:
            return False
        if self._is_qualified(t):
            return False
        if self._has_templates(t):
            return False
        # common STL containers should not be prefixed
        stl = {"std::vector", "std::map", "std::unordered_map", "std::set", "std::optional", "std::pair",
               "vector", "map", "unordered_map", "set", "optional", "pair"}
        if t in stl:
            return False
        return True

    def _resolve_type(self, namespace: str) -> str:
        t = self.typeStr.strip()
        t = self._normalize_basic_type(t)

        # If there are template args, leave as is (assume caller provided fully qualified args)
        if self._has_templates(t):
            resolved = t
        else:
            if self.typeDSL and self._should_prefix_namespace(t) and namespace:
                resolved = f"{namespace}::{t}"
            else:
                resolved = t

        if self.optional:
            # avoid double wrapping if already optional
            if not resolved.startswith("std::optional<"):
                resolved = f"std::optional<{resolved}>"
        return resolved

    def writeDefinition(self, target, fullInd: str, ind: str, namespace: str) -> None:
        '''Write a C++ definition for the class field.'''
        cpp_type = self._resolve_type(namespace or "")
        line = f"{fullInd}{cpp_type} {self.name};\n"
        target.write(line)
