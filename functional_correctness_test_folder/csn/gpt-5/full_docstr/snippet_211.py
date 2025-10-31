from typing import IO, Any, Optional


class FieldDefinition:
    '''Prototype of a single field from a class definition.'''

    def __init__(self, name: str, typeStr: str, optional: bool, mapSubject: str, mapPredicate: str, typeDSL: bool):
        '''Initialize field definition.
        Creates a new field with name, its type, optional and which field to use to convert
        from list to map (or empty if it is not possible)
        '''
        self.name = name
        self.typeStr = typeStr.strip()
        self.optional = bool(optional)
        self.mapSubject = (mapSubject or "").strip()
        self.mapPredicate = (mapPredicate or "").strip()
        self.typeDSL = bool(typeDSL)

    def _is_builtin(self, t: str) -> bool:
        builtin = {
            "void",
            "bool",
            "char",
            "signed char",
            "unsigned char",
            "short",
            "short int",
            "signed short",
            "signed short int",
            "unsigned short",
            "unsigned short int",
            "int",
            "signed",
            "signed int",
            "unsigned",
            "unsigned int",
            "long",
            "long int",
            "unsigned long",
            "unsigned long int",
            "long long",
            "long long int",
            "unsigned long long",
            "unsigned long long int",
            "float",
            "double",
            "long double",
            "size_t",
            "ptrdiff_t",
            "std::string",
            "std::wstring",
            "std::u16string",
            "std::u32string",
        }
        std_containers_prefixes = ("std::",)
        if t in builtin:
            return True
        if t.startswith(std_containers_prefixes):
            return True
        return False

    def _normalize_identifier(self, t: str) -> str:
        t = t.strip()
        if t == "string":
            return "std::string"
        return t

    def _resolve_simple(self, t: str, namespace: str) -> str:
        t = self._normalize_identifier(t)
        if self.typeDSL and "::" not in t and not self._is_builtin(t):
            ns = namespace.strip()
            if ns:
                return f"{ns}::{t}"
        return t

    def _split_top_level(self, s: str) -> list[str]:
        parts = []
        depth = 0
        current = []
        for ch in s:
            if ch == '<' or ch == '[':
                depth += 1
                current.append(ch)
            elif ch == '>' or ch == ']':
                depth -= 1
                current.append(ch)
            elif ch == ',' and depth == 0:
                parts.append("".join(current).strip())
                current = []
            else:
                current.append(ch)
        if current:
            parts.append("".join(current).strip())
        return parts

    def _parse_generic(self, t: str) -> Optional[tuple[str, list[str]]]:
        t = t.strip()
        # Accept forms: name<...> or name[...]
        if '<' in t and t.endswith('>'):
            head, rest = t.split('<', 1)
            inner = rest[:-1]
            return head.strip(), self._split_top_level(inner)
        if '[' in t and t.endswith(']'):
            head, rest = t.split('[', 1)
            inner = rest[:-1]
            return head.strip(), self._split_top_level(inner)
        return None

    def _resolve_type(self, t: str, namespace: str) -> str:
        t = t.strip()
        parsed = self._parse_generic(t)
        if parsed:
            head, args = parsed
            head_l = head.lower()
            if head_l in ("vector", "list", "array", "deque"):
                cpp_head = {
                    "vector": "std::vector",
                    "list": "std::vector",
                    "array": "std::array",
                    "deque": "std::deque",
                }[head_l]
                resolved_args = [self._resolve_type(
                    arg, namespace) for arg in args]
                return f"{cpp_head}<{', '.join(resolved_args)}>"
            if head_l in ("map", "unordered_map", "dict", "dictionary"):
                cpp_head = {
                    "map": "std::map",
                    "unordered_map": "std::unordered_map",
                    "dict": "std::map",
                    "dictionary": "std::map",
                }[head_l]
                resolved_args = [self._resolve_type(
                    arg, namespace) for arg in args]
                return f"{cpp_head}<{', '.join(resolved_args)}>"
            if head_l in ("optional",):
                resolved_args = [self._resolve_type(
                    arg, namespace) for arg in args]
                return f"std::optional<{', '.join(resolved_args)}>"
            # Generic unknown template: resolve head then args
            resolved_head = self._resolve_simple(head, namespace)
            resolved_args = [self._resolve_type(
                arg, namespace) for arg in args]
            return f"{resolved_head}<{', '.join(resolved_args)}>"
        # Not generic
        return self._resolve_simple(t, namespace)

    def writeDefinition(self, target: IO[Any], fullInd: str, ind: str, namespace: str) -> None:
        '''Write a C++ definition for the class field.'''
        if self.mapSubject and self.mapPredicate:
            base_type = f"std::map<{self._resolve_type(self.mapSubject, namespace)}, {self._resolve_type(self.mapPredicate, namespace)}>"
        else:
            base_type = self._resolve_type(self.typeStr, namespace)

        if self.optional and not base_type.startswith("std::optional<"):
            base_type = f"std::optional<{base_type}>"

        line = f"{fullInd}{base_type} {self.name};\n"
        target.write(line)
