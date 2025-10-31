
class Element:

    def set_common_datas(self, element, name, datas):
        element.name = name
        element.datas = datas

    def create_dictionary_of_element_from_dictionary(self, property_name, datas):
        elements = {}
        for key, value in datas.items():
            element = Element()
            self.set_common_datas(element, key, value)
            elements[key] = element
        return elements

    def create_list_of_element_from_dictionary(self, property_name, datas):
        elements = []
        for key, value in datas.items():
            element = Element()
            self.set_common_datas(element, key, value)
            elements.append(element)
        return elements

    def get_enum(self, property, enum, datas):
        if property in datas:
            return enum[datas[property]]
        return None
