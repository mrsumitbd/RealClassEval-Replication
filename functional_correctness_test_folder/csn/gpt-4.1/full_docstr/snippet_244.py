
class Element:
    ''' Populate Helper Factory
    '''

    def set_common_datas(self, element, name, datas):
        '''Populated common data for an element from dictionnary datas
        '''
        if not isinstance(datas, dict):
            return
        if name in datas:
            value = datas[name]
            if isinstance(value, dict):
                for k, v in value.items():
                    setattr(element, k, v)
            else:
                setattr(element, name, value)

    def create_dictionary_of_element_from_dictionary(self, property_name, datas):
        '''Populate a dictionary of elements
        '''
        result = {}
        if not isinstance(datas, dict):
            return result
        items = datas.get(property_name, {})
        if not isinstance(items, dict):
            return result
        for key, value in items.items():
            elem = type(self)()
            self.set_common_datas(elem, key, {key: value})
            result[key] = elem
        return result

    def create_list_of_element_from_dictionary(self, property_name, datas):
        '''Populate a list of elements
        '''
        result = []
        if not isinstance(datas, dict):
            return result
        items = datas.get(property_name, [])
        if not isinstance(items, list):
            return result
        for value in items:
            elem = type(self)()
            if isinstance(value, dict):
                for k, v in value.items():
                    setattr(elem, k, v)
            result.append(elem)
        return result

    def get_enum(self, property, enum, datas):
        '''Factory enum type
        '''
        if not isinstance(datas, dict):
            return None
        value = datas.get(property)
        if value is None:
            return None
        try:
            return enum(value)
        except Exception:
            return None
