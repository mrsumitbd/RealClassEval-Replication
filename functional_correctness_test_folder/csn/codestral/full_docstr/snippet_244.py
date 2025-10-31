
class Element:
    ''' Populate Helper Factory
    '''

    def set_common_datas(self, element, name, datas):
        '''Populated common data for an element from dictionnary datas
        '''
        if name in datas:
            setattr(element, name, datas[name])

    def create_dictionary_of_element_from_dictionary(self, property_name, datas):
        '''Populate a dictionary of elements
        '''
        elements = {}
        for key, value in datas.items():
            element = self.__class__()
            self.set_common_datas(element, property_name, value)
            elements[key] = element
        return elements

    def create_list_of_element_from_dictionary(self, property_name, datas):
        '''Populate a list of elements
        '''
        elements = []
        for value in datas:
            element = self.__class__()
            self.set_common_datas(element, property_name, value)
            elements.append(element)
        return elements

    def get_enum(self, property, enum, datas):
        '''Factory enum type
        '''
        if property in datas:
            return enum[datas[property]]
        return None
