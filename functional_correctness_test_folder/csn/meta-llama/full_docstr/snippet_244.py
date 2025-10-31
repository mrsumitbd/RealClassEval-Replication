
from enum import Enum


class Element:
    ''' Populate Helper Factory
    '''

    def set_common_datas(self, element, name, datas):
        '''Populated common data for an element from dictionnary datas
        '''
        if 'id' in datas:
            element.id = datas['id']
        if 'name' in datas:
            element.name = datas['name']
        if 'description' in datas:
            element.description = datas.get('description', '')

    def create_dictionary_of_element_from_dictionary(self, property_name, datas):
        '''Populate a dictionary of elements
        '''
        elements = {}
        if property_name in datas:
            for key, data in datas[property_name].items():
                element = ElementType()  # Assuming ElementType is the class of the elements
                self.set_common_datas(element, key, data)
                elements[key] = element
        return elements

    def create_list_of_element_from_dictionary(self, property_name, datas):
        '''Populate a list of elements
        '''
        elements = []
        if property_name in datas:
            for data in datas[property_name]:
                element = ElementType()  # Assuming ElementType is the class of the elements
                self.set_common_datas(element, None, data)
                elements.append(element)
        return elements

    def get_enum(self, property, enum, datas):
        '''Factory enum type
        '''
        if property in datas:
            return enum(datas[property])
        return None


# Example usage:

class ElementType:
    def __init__(self):
        self.id = None
        self.name = None
        self.description = ''


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


if __name__ == "__main__":
    element_helper = Element()

    datas = {
        'id': 1,
        'name': 'Test',
        'description': 'This is a test',
        'colors': {
            'red': {'id': 1, 'name': 'Red'},
            'green': {'id': 2, 'name': 'Green'}
        },
        'shapes': [
            {'id': 1, 'name': 'Circle'},
            {'id': 2, 'name': 'Square'}
        ],
        'color': 'RED'
    }

    element = ElementType()
    element_helper.set_common_datas(element, 'Test', datas)
    print(element.__dict__)

    colors = element_helper.create_dictionary_of_element_from_dictionary(
        'colors', datas)
    print({key: value.__dict__ for key, value in colors.items()})

    shapes = element_helper.create_list_of_element_from_dictionary(
        'shapes', datas)
    print([shape.__dict__ for shape in shapes])

    color_enum = element_helper.get_enum('color', Color, datas)
    print(color_enum)
