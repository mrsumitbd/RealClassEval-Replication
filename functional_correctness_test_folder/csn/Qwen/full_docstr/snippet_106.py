
import xml.etree.ElementTree as ET


class XMLStorage:
    '''Generic class for storing XML data from PLIP XML files.'''
    @staticmethod
    def getdata(tree, location, force_string=False):
        '''Gets XML data from a specific element and handles types.'''
        element = tree.find(location)
        if element is not None:
            data = element.text
            if force_string:
                return str(data)
            try:
                return int(data)
            except ValueError:
                try:
                    return float(data)
                except ValueError:
                    return data
        return None

    @staticmethod
    def getcoordinates(tree, location):
        '''Gets coordinates from a specific element in PLIP XML'''
        element = tree.find(location)
        if element is not None:
            coords = element.text.split()
            if len(coords) == 3:
                try:
                    return tuple(float(coord) for coord in coords)
                except ValueError:
                    pass
        return None
