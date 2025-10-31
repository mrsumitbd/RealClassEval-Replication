
class XMLStorage:
    '''Generic class for storing XML data from PLIP XML files.'''
    @staticmethod
    def getdata(tree, location, force_string=False):
        '''Gets XML data from a specific element and handles types.'''
        element = tree.find(location)
        if element is not None:
            if force_string:
                return str(element.text)
            else:
                try:
                    return float(element.text)
                except ValueError:
                    return element.text
        return None

    @staticmethod
    def getcoordinates(tree, location):
        '''Gets coordinates from a specific element in PLIP XML'''
        element = tree.find(location)
        if element is not None:
            coordinates = element.text.split(',')
            return [float(coord.strip()) for coord in coordinates]
        return None
