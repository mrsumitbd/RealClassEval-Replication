
class Element:

    def set_common_datas(self, element, name, datas):
        element.name = name
        element.datas = datas

    def create_dictionary_of_element_from_dictionary(self, property_name, datas):
        return {key: datas[key] for key in datas if key != property_name}

    def create_list_of_element_from_dictionary(self, property_name, datas):
        return [value for key, value in datas.items() if key != property_name]

    def get_enum(self, property, enum, datas):
        return enum(datas.get(property, None))
