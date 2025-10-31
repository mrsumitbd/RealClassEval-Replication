
import xml.etree.ElementTree as ET


class XMLStorage:

    @staticmethod
    def getdata(tree, location, force_string=False):
        """
        Retrieve the text or value at the given location in the XML tree.
        If force_string is True, always return as string.
        """
        elem = tree.find(location)
        if elem is None:
            return None
        if len(elem) == 0 and elem.text is not None:
            value = elem.text.strip()
        else:
            value = elem.text if elem.text is not None else ''
        if not force_string:
            # Try to convert to int or float if possible
            try:
                return int(value)
            except (ValueError, TypeError):
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return value
        else:
            return value

    @staticmethod
    def getcoordinates(tree, location):
        """
        Retrieve coordinates (x, y) from the given location in the XML tree.
        The location should point to a parent element containing 'x' and 'y' children.
        """
        elem = tree.find(location)
        if elem is None:
            return None
        x_elem = elem.find('x')
        y_elem = elem.find('y')
        if x_elem is None or y_elem is None:
            return None
        try:
            x = float(x_elem.text.strip())
            y = float(y_elem.text.strip())
            return (x, y)
        except (ValueError, AttributeError):
            return None
