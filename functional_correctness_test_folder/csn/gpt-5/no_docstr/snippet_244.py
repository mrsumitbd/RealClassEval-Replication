from enum import Enum
from collections.abc import Mapping, Iterable


class Element:

    def set_common_datas(self, element, name, datas):
        if element is None:
            return None
        if name is not None:
            try:
                setattr(element, 'name', name)
            except Exception:
                pass
        if isinstance(datas, Mapping):
            for k, v in datas.items():
                try:
                    setattr(element, k, v)
                except Exception:
                    continue
        return element

    def create_dictionary_of_element_from_dictionary(self, property_name, datas):
        if not isinstance(datas, Mapping):
            return {}
        value = datas.get(property_name)
        if value is None:
            return {}
        if isinstance(value, Mapping):
            return dict(value)
        if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
            try:
                return dict(value)
            except Exception:
                return {}
        return {}

    def create_list_of_element_from_dictionary(self, property_name, datas):
        if not isinstance(datas, Mapping):
            return []
        value = datas.get(property_name)
        if value is None:
            return []
        if isinstance(value, list):
            return value
        if isinstance(value, tuple):
            return list(value)
        if isinstance(value, Iterable) and not isinstance(value, (str, bytes, Mapping)):
            return list(value)
        return [value]

    def get_enum(self, property, enum, datas):
        if not isinstance(datas, Mapping):
            return None
        raw = datas.get(property)
        if raw is None:
            return None

        if isinstance(enum, type) and issubclass(enum, Enum):
            if isinstance(raw, enum):
                return raw
            if isinstance(raw, str):
                key = raw.strip()
                # Try exact, then case-insensitive by name
                try:
                    return enum[key]
                except Exception:
                    pass
                lowered = key.lower()
                for member in enum:
                    if member.name.lower() == lowered:
                        return member
                # Try by value if value is string and matches
                for member in enum:
                    try:
                        if str(member.value) == key:
                            return member
                    except Exception:
                        continue
            else:
                # Try by value
                for member in enum:
                    try:
                        if member.value == raw:
                            return member
                    except Exception:
                        continue
        else:
            # Fallback for mapping-like enums
            if isinstance(enum, Mapping):
                if raw in enum:
                    return enum[raw]
                if isinstance(raw, str):
                    lowered = raw.lower()
                    for k, v in enum.items():
                        try:
                            if isinstance(k, str) and k.lower() == lowered:
                                return v
                        except Exception:
                            continue
        return None
