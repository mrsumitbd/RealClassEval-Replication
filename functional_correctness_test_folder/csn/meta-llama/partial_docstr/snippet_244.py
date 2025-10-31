
class Element:

    def set_common_datas(self, element, name, datas):
        element.name = name
        for key, value in datas.items():
            setattr(element, key, value)

    def create_dictionary_of_element_from_dictionary(self, property_name, datas):
        elements = {}
        for key, value in datas.items():
            element = type(property_name, (), {})()
            self.set_common_datas(element, key, value)
            elements[key] = element
        return elements

    def create_list_of_element_from_dictionary(self, property_name, datas):
        elements = []
        for key, value in datas.items():
            element = type(property_name, (), {})()
            self.set_common_datas(element, key, value)
            elements.append(element)
        return elements

    def get_enum(self, property, enum, datas):
        return enum(datas[property])
