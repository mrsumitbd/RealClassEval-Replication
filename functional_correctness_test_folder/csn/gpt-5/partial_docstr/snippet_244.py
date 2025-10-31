class Element:
    def set_common_datas(self, element, name, datas):
        if element is None:
            return
        setattr(element, "name", name)
        if isinstance(datas, dict):
            for k, v in datas.items():
                if k == "name":
                    continue
                setattr(element, k, v)
        else:
            setattr(element, "value", datas)

    def create_dictionary_of_element_from_dictionary(self, property_name, datas):
        result = {}
        if not isinstance(datas, dict):
            return result
        items = datas.get(property_name)
        if not isinstance(items, dict):
            return result
        for name, props in items.items():
            child = Element()
            if isinstance(props, dict):
                self.set_common_datas(child, name, props)
            else:
                self.set_common_datas(child, name, {"value": props})
            result[name] = child
        return result

    def create_list_of_element_from_dictionary(self, property_name, datas):
        result = []
        if not isinstance(datas, dict):
            return result
        items = datas.get(property_name)
        if isinstance(items, dict):
            for name, props in items.items():
                child = Element()
                if isinstance(props, dict):
                    self.set_common_datas(child, name, props)
                else:
                    self.set_common_datas(child, name, {"value": props})
                result.append(child)
        elif isinstance(items, list):
            for entry in items:
                if isinstance(entry, dict):
                    name = entry.get("name")
                    child = Element()
                    self.set_common_datas(child, name, entry)
                    result.append(child)
                else:
                    child = Element()
                    self.set_common_datas(child, None, {"value": entry})
                    result.append(child)
        return result

    def get_enum(self, property, enum, datas):
        if not isinstance(datas, dict):
            return None
        value = datas.get(property)
        if value is None:
            return None

        def convert(v):
            if isinstance(v, enum):
                return v
            try:
                return enum(v)
            except Exception:
                if isinstance(v, str):
                    try:
                        return enum[v]
                    except Exception:
                        # case-insensitive name or value matching
                        for e in enum:
                            if e.name.lower() == v.lower():
                                return e
                            if isinstance(e.value, str) and e.value.lower() == v.lower():
                                return e
                # last resort: match by string representation
                for e in enum:
                    if str(e.value) == str(v) or str(e.name) == str(v):
                        return e
                raise ValueError(f"Invalid enum value: {v}")

        if isinstance(value, list):
            return [convert(v) for v in value]
        return convert(value)
