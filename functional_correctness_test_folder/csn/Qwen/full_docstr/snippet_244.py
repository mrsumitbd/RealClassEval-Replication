
class Element:
    ''' Populate Helper Factory
    '''

    def set_common_datas(self, element, name, datas):
        '''Populated common data for an element from dictionary datas
        '''
        if datas and name in datas:
            for key, value in datas[name].items():
                if hasattr(element, key):
                    setattr(element, key, value)

    def create_dictionary_of_element_from_dictionary(self, property_name, datas):
        '''Populate a dictionary of elements
        '''
        result = {}
        if datas and property_name in datas:
            for key, value in datas[property_name].items():
                new_element = self.__class__()
                self.set_common_datas(new_element, key, {key: value})
                result[key] = new_element
        return result

    def create_list_of_element_from_dictionary(self, property_name, datas):
        '''Populate a list of elements
        '''
        result = []
        if datas and property_name in datas:
            for item in datas[property_name]:
                new_element = self.__class__()
                self.set_common_datas(new_element, property_name, {
                                      property_name: item})
                result.append(new_element)
        return result

    def get_enum(self, property, enum, datas):
        '''Factory enum type
        '''
        if datas and property in datas:
            value = datas[property]
            if value in enum:
                return enum[value]
        return None
