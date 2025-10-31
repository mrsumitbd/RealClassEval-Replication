
import xml.etree.ElementTree as ET


class XMLStorage:

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
        element = tree.find(location)
        if element is not None:
            x = float(element.get('x'))
            y = float(element.get('y'))
            return (x, y)
        return None
