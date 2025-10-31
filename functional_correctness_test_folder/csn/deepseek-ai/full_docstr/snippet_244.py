
class Element:
    ''' Populate Helper Factory
    '''

    def set_common_datas(self, element, name, datas):
        '''Populated common data for an element from dictionnary datas
        '''
        if name in datas:
            element.__dict__.update(datas[name])

    def create_dictionary_of_element_from_dictionary(self, property_name, datas):
        '''Populate a dictionary of elements
        '''
        result = {}
        if property_name in datas:
            for key, value in datas[property_name].items():
                element = Element()
                element.__dict__.update(value)
                result[key] = element
        return result

    def create_list_of_element_from_dictionary(self, property_name, datas):
        '''Populate a list of elements
        '''
        result = []
        if property_name in datas:
            for item in datas[property_name]:
                element = Element()
                if isinstance(item, dict):
                    element.__dict__.update(item)
                result.append(element)
        return result

    def get_enum(self, property, enum, datas):
        '''Factory enum type
        '''
        if property in datas:
            return enum(datas[property])
        return None
