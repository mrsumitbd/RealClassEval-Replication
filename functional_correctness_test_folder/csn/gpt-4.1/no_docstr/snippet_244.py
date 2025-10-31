
class Element:

    def set_common_datas(self, element, name, datas):
        if element is not None and name in datas:
            setattr(element, name, datas[name])

    def create_dictionary_of_element_from_dictionary(self, property_name, datas):
        result = {}
        if property_name in datas and isinstance(datas[property_name], dict):
            for key, value in datas[property_name].items():
                result[key] = value
        return result

    def create_list_of_element_from_dictionary(self, property_name, datas):
        result = []
        if property_name in datas and isinstance(datas[property_name], list):
            for item in datas[property_name]:
                result.append(item)
        return result

    def get_enum(self, property, enum, datas):
        value = datas.get(property)
        if value is not None:
            try:
                return enum(value)
            except Exception:
                return None
        return None
