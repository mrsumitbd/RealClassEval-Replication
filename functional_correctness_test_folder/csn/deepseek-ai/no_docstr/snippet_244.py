
class Element:

    def set_common_datas(self, element, name, datas):
        if datas is not None and name in datas:
            element[name] = datas[name]

    def create_dictionary_of_element_from_dictionary(self, property_name, datas):
        if datas is not None and property_name in datas:
            return datas[property_name]
        return {}

    def create_list_of_element_from_dictionary(self, property_name, datas):
        if datas is not None and property_name in datas:
            return datas[property_name]
        return []

    def get_enum(self, property, enum, datas):
        if datas is not None and property in datas:
            value = datas[property]
            if value in enum.__members__:
                return enum[value]
        return None
