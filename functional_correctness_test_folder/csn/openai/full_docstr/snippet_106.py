
import xml.etree.ElementTree as ET
from typing import Any, Tuple, Optional


class XMLStorage:
    """Generic class for storing XML data from PLIP XML files."""

    @staticmethod
    def getdata(tree: ET.ElementTree | ET.Element, location: str,
                force_string: bool = False) -> Any:
        """
        Retrieve data from a specific XML element.

        Parameters
        ----------
        tree : ElementTree or Element
            The XML tree or element to search.
        location : str
            XPath-like location string relative to the provided tree.
        force_string : bool, optional
            If True, always return the element's text as a string.
            If False, attempt to cast to int or float.

        Returns
        -------
        Any
            The extracted data, cast to int/float if possible, otherwise a string.
            Returns None if the element or its text is missing.
        """
        if not location:
            return None

        # Find the element; ElementTree.find works on both ElementTree and Element
        elem = tree.find(location)
        if elem is None:
            return None

        text = elem.text
        if text is None:
            return None

        text = text.strip()
        if force_string:
            return text

        # Try integer conversion
        try:
            return int(text)
        except ValueError:
            pass

        # Try float conversion
        try:
            return float(text)
        except ValueError:
            pass

        return text

    @staticmethod
    def getcoordinates(tree: ET.ElementTree | ET.Element,
                       location: str) -> Optional[Tuple[float, float, float]]:
        """
        Retrieve 3‑D coordinates from a specific XML element.

        Parameters
        ----------
        tree : ElementTree or Element
            The XML tree or element to search.
        location : str
            XPath-like location string relative to the provided tree.

        Returns
        -------
        tuple[float, float, float] or None
            A tuple (x, y, z) of coordinates if found, otherwise None.
        """
        if not location:
            return None

        elem = tree.find(location)
        if elem is None:
            return None

        coords = {}
        for coord in ("x", "y", "z"):
            # First try attribute
            val = elem.get(coord)
            # Then try subelement
            if val is None:
                sub = elem.find(coord)
                if sub is not None:
                    val = sub.text
            if val is None:
                return None
            try:
                coords[coord] = float(val.strip())
            except ValueError:
                return None

        return coords["x"], coords["y"], coords["z"]
