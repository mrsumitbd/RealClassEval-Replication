
class XMLStorage:
    '''Generic class for storing XML data from PLIP XML files.'''
    @staticmethod
    def getdata(tree, location, force_string=False):
        element = tree.find(location)
        if element is not None:
            if force_string:
                return element.text
            try:
                return float(element.text)
            except (ValueError, TypeError):
                return element.text
        return None

    @staticmethod
    def getcoordinates(tree, location):
        '''Gets coordinates from a specific element in PLIP XML'''
        coords = {}
        for coord in ['x', 'y', 'z']:
            element = tree.find(f"{location}/{coord}")
            if element is not None and element.text is not None:
                try:
                    coords[coord] = float(element.text)
                except ValueError:
                    coords[coord] = None
        return coords
