
class Element:

    def set_common_datas(self, element, name, datas):

        element.name = name
        element.datas = datas

    def create_dictionary_of_element_from_dictionary(self, property_name, datas):

        dictionary = {}
        for key, value in datas.items():
            element = Element()
            self.set_common_datas(element, key, value)
            dictionary[key] = element
        return dictionary

    def create_list_of_element_from_dictionary(self, property_name, datas):

        list_of_elements = []
        for key, value in datas.items():
            element = Element()
            self.set_common_datas(element, key, value)
            list_of_elements.append(element)
        return list_of_elements

    def get_enum(self, property, enum, datas):

        if property in datas:
            return enum[datas[property]]
        return None
