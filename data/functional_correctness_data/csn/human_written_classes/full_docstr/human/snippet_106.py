class XMLStorage:
    """Generic class for storing XML data from PLIP XML files."""

    @staticmethod
    def getdata(tree, location, force_string=False):
        """Gets XML data from a specific element and handles types."""
        found = tree.xpath('%s/text()' % location)
        if not found:
            return None
        else:
            data = found[0]
        if force_string:
            return data
        if data == 'True':
            return True
        elif data == 'False':
            return False
        else:
            try:
                return int(data)
            except ValueError:
                try:
                    return float(data)
                except ValueError:
                    return data

    @staticmethod
    def getcoordinates(tree, location):
        """Gets coordinates from a specific element in PLIP XML"""
        return tuple((float(x) for x in tree.xpath('.//%s/*/text()' % location)))