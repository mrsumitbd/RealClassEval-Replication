
import xml.etree.ElementTree as ET
from typing import Any, Tuple, Optional


class XMLStorage:
    @staticmethod
    def _find_element(tree: Any, location: str) -> Optional[ET.Element]:
        """
        Helper to locate an element in the XML tree.
        Accepts either an ElementTree or an Element.
        """
        if isinstance(tree, ET.ElementTree):
            root = tree.getroot()
        elif isinstance(tree, ET.Element):
            root = tree
        else:
            raise TypeError("tree must be an ElementTree or Element")

        # Use the standard find method which supports simple XPath
        return root.find(location)

    @staticmethod
    def getdata(tree: Any, location: str, force_string: bool = False) -> Any:
        """
        Retrieve data from the XML tree at the specified location.

        Parameters
        ----------
        tree : ElementTree or Element
            The XML tree to search.
        location : str
            XPath-like string to locate the element.
        force_string : bool, optional
            If True, always return a string representation of the data.
            Default is False.

        Returns
        -------
        Any
            The text content of the element, its attributes as a dict,
            or a string representation depending on `force_string`.
            Returns None if the element is not found.
        """
        elem = XMLStorage._find_element(tree, location)
        if elem is None:
            return None

        # Prefer text content if available
        if elem.text and elem.text.strip():
            data = elem.text.strip()
        else:
            # Fallback to attributes dictionary
            data = dict(elem.attrib)

        if force_string:
            return str(data)
        return data

    @staticmethod
    def getcoordinates(tree: Any, location: str) -> Optional[Tuple[float, float]]:
        """
        Retrieve (x, y) coordinates from an element's attributes.

        Parameters
        ----------
        tree : ElementTree or Element
            The XML tree to search.
        location : str
            XPath-like string to locate the element.

        Returns
        -------
        tuple[float, float] or None
            A tuple of (x, y) coordinates if both attributes are present
            and convertible to float. Returns None otherwise.
        """
        elem = XMLStorage._find_element(tree, location)
        if elem is None:
            return None

        try:
            x = float(elem.attrib.get("x"))
            y = float(elem.attrib.get("y"))
            return (x, y)
        except (TypeError, ValueError):
            return None
