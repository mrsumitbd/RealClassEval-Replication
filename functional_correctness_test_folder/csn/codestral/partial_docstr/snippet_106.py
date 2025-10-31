
import xml.etree.ElementTree as ET


class XMLStorage:
    '''Generic class for storing XML data from PLIP XML files.'''

    @staticmethod
    def getdata(tree, location, force_string=False):
        element = tree.find(location)
        if element is not None:
            if force_string:
                return str(element.text)
            else:
                return element.text
        return None

    @staticmethod
    def getcoordinates(tree, location):
        '''Gets coordinates from a specific element in PLIP XML'''
        element = tree.find(location)
        if element is not None:
            x = float(element.get('x'))
            y = float(element.get('y'))
            z = float(element.get('z'))
            return (x, y, z)
        return None
