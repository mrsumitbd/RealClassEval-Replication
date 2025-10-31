
import xml.etree.ElementTree as ET


class XMLStorage:
    '''Generic class for storing XML data from PLIP XML files.'''
    @staticmethod
    def getdata(tree, location, force_string=False):
        element = tree.find(location)
        if element is not None:
            if force_string:
                return element.text if element.text is not None else ''
            else:
                return element.text
        return None

    @staticmethod
    def getcoordinates(tree, location):
        '''Gets coordinates from a specific element in PLIP XML'''
        element = tree.find(location)
        if element is not None:
            try:
                x = float(element.get('x', 0))
                y = float(element.get('y', 0))
                z = float(element.get('z', 0))
                return (x, y, z)
            except ValueError:
                return (0.0, 0.0, 0.0)
        return (0.0, 0.0, 0.0)
