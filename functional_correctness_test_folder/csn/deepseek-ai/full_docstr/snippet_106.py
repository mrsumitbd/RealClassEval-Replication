
class XMLStorage:
    '''Generic class for storing XML data from PLIP XML files.'''
    @staticmethod
    def getdata(tree, location, force_string=False):
        '''Gets XML data from a specific element and handles types.'''
        element = tree.find(location)
        if element is None:
            return None
        text = element.text
        if text is None:
            return None
        if force_string:
            return text.strip()
        try:
            return int(text)
        except ValueError:
            try:
                return float(text)
            except ValueError:
                return text.strip()

    @staticmethod
    def getcoordinates(tree, location):
        '''Gets coordinates from a specific element in PLIP XML'''
        element = tree.find(location)
        if element is None:
            return None
        coords = []
        for coord in ['x', 'y', 'z']:
            val = XMLStorage.getdata(element, coord)
            if val is None:
                return None
            coords.append(val)
        return coords
