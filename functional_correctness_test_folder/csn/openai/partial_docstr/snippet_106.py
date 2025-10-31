
import xml.etree.ElementTree as ET
from typing import Any, List, Tuple, Optional


class XMLStorage:
    """Generic class for storing XML data from PLIP XML files."""

    @staticmethod
    def getdata(tree: ET.Element, location: str, force_string: bool = False) -> Any:
        """
        Retrieve data from the XML tree at the given XPath location.

        Parameters
        ----------
        tree : xml.etree.ElementTree.Element
            The root element of the XML tree.
        location : str
            XPath expression relative to the root element.
        force_string : bool, optional
            If True, return the data as a string regardless of its original type.

        Returns
        -------
        Any
            The extracted data. If multiple elements match the XPath, a list of
            values is returned. If a single element matches, its value is returned.
            If no element matches, None is returned.
        """
        # Find all matching elements
        elements = tree.findall(location)
        if not elements:
            return None

        # Helper to extract value from an element
        def _extract(elem: ET.Element) -> Any:
            # Prefer attribute 'value' if present
            if "value" in elem.attrib:
                val = elem.attrib["value"]
            else:
                val = elem.text
            if val is None:
                return None
            if force_string:
                return str(val).strip()
            # Try to convert to int or float
            try:
                if "." in val or "e" in val.lower():
                    return float(val)
                return int(val)
            except Exception:
                return str(val).strip()

        # If only one element, return its value directly
        if len(elements) == 1:
            return _extract(elements[0])

        # Otherwise return list of values
        return [_extract(e) for e in elements]

    @staticmethod
    def getcoordinates(tree: ET.Element, location: str) -> Optional[Tuple[float, float, float]]:
        """
        Extract 3D coordinates from a specific element in a PLIP XML file.

        Parameters
        ----------
        tree : xml.etree.ElementTree.Element
            The root element of the XML tree.
        location : str
            XPath expression pointing to the element that contains coordinate data.

        Returns
        -------
        tuple[float, float, float] or None
            A tuple of (x, y, z) coordinates if found, otherwise None.
        """
        elem = tree.find(location)
        if elem is None:
            return None

        # Try to get coordinates from attributes first
        if all(k in elem.attrib for k in ("x", "y", "z")):
            try:
                return (
                    float(elem.attrib["x"]),
                    float(elem.attrib["y"]),
                    float(elem.attrib["z"]),
                )
            except Exception:
                pass

        # Fallback: look for child elements <x>, <y>, <z>
        coords = {}
        for axis in ("x", "y", "z"):
            child = elem.find(axis)
            if child is not None and child.text is not None:
                try:
                    coords[axis] = float(child.text)
                except Exception:
                    return None
        if len(coords) == 3:
            return coords["x"], coords["y"], coords["z"]

        return None
