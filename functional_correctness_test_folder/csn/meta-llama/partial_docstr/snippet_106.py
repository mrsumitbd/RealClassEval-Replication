
import xml.etree.ElementTree as ET


class XMLStorage:
    '''Generic class for storing XML data from PLIP XML files.'''
    @staticmethod
    def getdata(tree, location, force_string=False):
        """Gets data from a specific element in PLIP XML.

        Args:
            tree (xml.etree.ElementTree.Element): The root element of the XML tree.
            location (str): The XPath expression to the desired element.
            force_string (bool): If True, the result will be converted to a string.

        Returns:
            The data from the specified location. If multiple elements are found, a list is returned.
        """
        elements = tree.findall(location)
        if len(elements) == 0:
            return None
        elif len(elements) == 1:
            element = elements[0]
            if force_string:
                return element.text
            else:
                if element.text is None:
                    return None
                try:
                    return int(element.text)
                except ValueError:
                    try:
                        return float(element.text)
                    except ValueError:
                        return element.text
        else:
            data = []
            for element in elements:
                if force_string:
                    data.append(element.text)
                else:
                    if element.text is None:
                        data.append(None)
                    else:
                        try:
                            data.append(int(element.text))
                        except ValueError:
                            try:
                                data.append(float(element.text))
                            except ValueError:
                                data.append(element.text)
            return data

    @staticmethod
    def getcoordinates(tree, location):
        '''Gets coordinates from a specific element in PLIP XML.

        Args:
            tree (xml.etree.ElementTree.Element): The root element of the XML tree.
            location (str): The XPath expression to the desired element.

        Returns:
            A list of coordinates (x, y, z) if the element is found, otherwise None.
        '''
        coords = XMLStorage.getdata(tree, location)
        if coords is None:
            return None
        if isinstance(coords, list):
            return [tuple(map(float, coord.split())) for coord in coords]
        else:
            return tuple(map(float, coords.split()))
