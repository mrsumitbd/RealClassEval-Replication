class Element:
    ''' Populate Helper Factory
    '''

    def set_common_datas(self, element, name, datas):
        '''Populated common data for an element from dictionnary datas
        '''
        setattr(element, "name", name)
        if isinstance(datas, dict):
            for k, v in datas.items():
                try:
                    setattr(element, k, v)
                except Exception:
                    # Ignore attributes that cannot be set
                    pass
        return element

    def create_dictionary_of_element_from_dictionary(self, property_name, datas):
        '''Populate a dictionary of elements
        '''
        if not isinstance(datas, dict):
            return {}
        value = datas.get(property_name)
        if value is None:
            return {}
        if isinstance(value, dict):
            return dict(value)
        if isinstance(value, (list, tuple)):
            result = {}
            for item in value:
                if isinstance(item, dict) and "key" in item and "value" in item:
                    result[item["key"]] = item["value"]
                elif isinstance(item, (list, tuple)) and len(item) == 2:
                    k, v = item
                    result[k] = v
            return result
        return {}

    def create_list_of_element_from_dictionary(self, property_name, datas):
        '''Populate a list of elements
        '''
        if not isinstance(datas, dict):
            return []
        value = datas.get(property_name)
        if value is None:
            return []
        if isinstance(value, list):
            return list(value)
        if isinstance(value, (tuple, set)):
            return list(value)
        if isinstance(value, dict):
            return list(value.values())
        return [value]

    def get_enum(self, property, enum, datas):
        '''Factory enum type
        '''
        if not isinstance(datas, dict):
            return None
        val = datas.get(property)
        if val is None:
            return None

        try:
            from enum import Enum
        except Exception:
            Enum = None  # Fallback if enum is unavailable

        # If enum is already the correct instance
        if Enum is not None and isinstance(val, enum if isinstance(enum, type) else type(val)):
            return val

        # Enum class handling
        if Enum is not None and isinstance(enum, type) and issubclass(enum, Enum):
            # Direct match
            if isinstance(val, enum):
                return val
            # Try by name
            if isinstance(val, str):
                try:
                    return enum[val]
                except KeyError:
                    try:
                        return enum[val.upper()]
                    except Exception:
                        pass
                    # Case-insensitive name match
                    name_map = {m.name.lower(): m for m in enum}
                    found = name_map.get(val.lower())
                    if found is not None:
                        return found
                # Try by value when values are strings
                for member in enum:
                    if str(member.value) == str(val):
                        return member
            # Try by value (int/str)
            try:
                return enum(val)
            except Exception:
                pass
            return None

        # Mapping/dict fallback
        if isinstance(enum, dict):
            if val in enum:
                return enum[val]
            if isinstance(val, str):
                # case-insensitive key lookup
                for k in enum:
                    if isinstance(k, str) and k.lower() == val.lower():
                        return enum[k]
            return None

        # Callable factory fallback
        if callable(enum):
            try:
                return enum(val)
            except Exception:
                return None

        return None
