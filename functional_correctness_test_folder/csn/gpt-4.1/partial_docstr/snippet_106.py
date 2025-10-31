
class XMLStorage:
    '''Generic class for storing XML data from PLIP XML files.'''
    @staticmethod
    def getdata(tree, location, force_string=False):
        """
        Extracts data from an XML tree at the given location.
        - tree: an ElementTree.Element (root)
        - location: XPath-like string (e.g., './ligand/hetid')
        - force_string: if True, always return as string
        Returns:
            - If multiple elements: list of values
            - If one element: value
            - If not found: None
        """
        elements = tree.findall(location)
        if not elements:
            return None
        results = []
        for el in elements:
            if el.text is not None:
                val = el.text.strip()
            else:
                val = ''
            if not force_string:
                # Try to convert to int or float if possible
                try:
                    if '.' in val:
                        val = float(val)
                    else:
                        val = int(val)
                except (ValueError, TypeError):
                    pass
            results.append(val)
        if len(results) == 1:
            return results[0]
        return results

    @staticmethod
    def getcoordinates(tree, location):
        '''Gets coordinates from a specific element in PLIP XML'''
        # Expects location to point to an element with children x, y, z
        element = tree.find(location)
        if element is None:
            return None
        try:
            x = float(element.find('x').text.strip())
            y = float(element.find('y').text.strip())
            z = float(element.find('z').text.strip())
            return (x, y, z)
        except (AttributeError, ValueError):
            return None
