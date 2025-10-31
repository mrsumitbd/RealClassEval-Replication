
class Element:

    def set_common_datas(self, element, name, datas):
        element.name = name
        element.datas = datas

    def create_dictionary_of_element_from_dictionary(self, property_name, datas):
        result = {}
        for key, value in datas.items():
            new_element = Element()
            self.set_common_datas(new_element, key, value)
            result[key] = new_element
        return result

    def create_list_of_element_from_dictionary(self, property_name, datas):
        result = []
        for key, value in datas.items():
            new_element = Element()
            self.set_common_datas(new_element, key, value)
            result.append(new_element)
        return result

    def get_enum(self, property, enum, datas):
        if property in datas:
            value = datas[property]
            if value in enum:
                return enum[value]
        return None
