
import xml.etree.ElementTree as ET


class XMLStorage:

    @staticmethod
    def getdata(tree, location, force_string=False):
        element = tree.find(location)
        if element is not None:
            if force_string:
                return str(element.text)
            return element.text
        return None

    @staticmethod
    def getcoordinates(tree, location):
        element = tree.find(location)
        if element is not None:
            try:
                x = float(element.get('x', 0))
                y = float(element.get('y', 0))
                return (x, y)
            except ValueError:
                return None
        return None
