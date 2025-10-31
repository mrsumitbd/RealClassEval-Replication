
class XMLStorage:
    '''Generic class for storing XML data from PLIP XML files.'''
    @staticmethod
    def getdata(tree, location, force_string=False):
        '''Gets XML data from a specific element and handles types.'''
        elem = tree.find(location)
        if elem is None or elem.text is None:
            return None
        text = elem.text.strip()
        if force_string:
            return text
        # Try to convert to int, then float, else return string
        try:
            return int(text)
        except ValueError:
            try:
                return float(text)
            except ValueError:
                return text

    @staticmethod
    def getcoordinates(tree, location):
        '''Gets coordinates from a specific element in PLIP XML'''
        elem = tree.find(location)
        if elem is None or elem.text is None:
            return None
        text = elem.text.strip()
        # Coordinates are usually space or comma separated
        # Try both
        if ',' in text:
            parts = text.split(',')
        else:
            parts = text.split()
        try:
            coords = [float(x) for x in parts]
            return coords
        except ValueError:
            return None
