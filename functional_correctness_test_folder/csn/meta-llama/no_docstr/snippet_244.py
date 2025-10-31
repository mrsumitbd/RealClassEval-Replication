
class Element:

    def set_common_datas(self, element, name, datas):
        element.name = name
        element.id = datas.get('id')
        element.description = datas.get('description')

    def create_dictionary_of_element_from_dictionary(self, property_name, datas):
        dictionary = {}
        for key, value in datas.get(property_name, {}).items():
            element = Element()
            self.set_common_datas(element, key, value)
            dictionary[key] = element
        return dictionary

    def create_list_of_element_from_dictionary(self, property_name, datas):
        elements = []
        for data in datas.get(property_name, []):
            element = Element()
            self.set_common_datas(element, data.get('name'), data)
            elements.append(element)
        return elements

    def get_enum(self, property, enum, datas):
        value = datas.get(property)
        if value is not None:
            return enum(value)
        return None
