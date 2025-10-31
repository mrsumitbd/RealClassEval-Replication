
import xml.etree.ElementTree as ET


class XMLStorage:
    '''Generic class for storing XML data from PLIP XML files.'''
    @staticmethod
    def getdata(tree, location, force_string=False):
        '''Gets XML data from a specific element and handles types.'''
        element = tree.find(location)
        if element is None:
            return None
        if element.text is None:
            return None
        if force_string:
            return element.text
        try:
            return int(element.text)
        except ValueError:
            try:
                return float(element.text)
            except ValueError:
                return element.text

    @staticmethod
    def getcoordinates(tree, location):
        '''Gets coordinates from a specific element in PLIP XML'''
        element = tree.find(location)
        if element is None:
            return None
        coords = []
        for coord in element.text.split(','):
            try:
                coords.append(float(coord))
            except ValueError:
                return None
        return coords
