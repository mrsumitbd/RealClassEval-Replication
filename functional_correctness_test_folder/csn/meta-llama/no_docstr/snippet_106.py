
import xml.etree.ElementTree as ET


class XMLStorage:

    @staticmethod
    def getdata(tree, location, force_string=False):
        """
        Retrieves data from an XML tree based on the given location.

        Args:
            tree (ET.Element): The root element of the XML tree.
            location (str): The XPath expression to locate the desired element.
            force_string (bool, optional): If True, the result will be returned as a string. Defaults to False.

        Returns:
            The data at the specified location. If force_string is True, it returns a string; otherwise, it returns the text content of the element or None if not found.
        """
        element = tree.find(location)
        if element is None:
            return None
        if force_string:
            return ET.tostring(element, encoding='unicode')
        else:
            return element.text

    @staticmethod
    def getcoordinates(tree, location):
        """
        Retrieves coordinates from an XML tree based on the given location.

        Args:
            tree (ET.Element): The root element of the XML tree.
            location (str): The XPath expression to locate the desired element.

        Returns:
            tuple: A tuple containing the latitude and longitude coordinates. If the coordinates are not found, it returns (None, None).
        """
        data = XMLStorage.getdata(tree, location)
        if data is None:
            return None, None
        try:
            coordinates = data.split(',')
            if len(coordinates) != 2:
                return None, None
            latitude = float(coordinates[0].strip())
            longitude = float(coordinates[1].strip())
            return latitude, longitude
        except ValueError:
            return None, None
