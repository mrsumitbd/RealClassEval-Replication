
class Element:

    def set_common_datas(self, element, name, datas):
        if datas is not None and name in datas:
            element[name] = datas[name]

    def create_dictionary_of_element_from_dictionary(self, property_name, datas):
        '''Populate a dictionary of elements
        '''
        result = {}
        if datas is not None and property_name in datas:
            for key, value in datas[property_name].items():
                result[key] = value
        return result

    def create_list_of_element_from_dictionary(self, property_name, datas):
        '''Populate a list of elements
        '''
        result = []
        if datas is not None and property_name in datas:
            result = list(datas[property_name])
        return result

    def get_enum(self, property, enum, datas):
        '''Factory enum type
        '''
        if datas is not None and property in datas:
            return enum(datas[property])
        return None
