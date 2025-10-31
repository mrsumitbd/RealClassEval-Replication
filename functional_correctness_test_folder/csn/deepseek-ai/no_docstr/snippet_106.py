
class XMLStorage:

    @staticmethod
    def getdata(tree, location, force_string=False):
        elements = tree.findall(location)
        if not elements:
            return None
        if len(elements) == 1 and not force_string:
            return elements[0].text
        return [element.text for element in elements]

    @staticmethod
    def getcoordinates(tree, location):
        elements = tree.findall(location)
        if not elements:
            return None
        coords = []
        for element in elements:
            try:
                lat = float(element.get('lat'))
                lon = float(element.get('lon'))
                coords.append((lat, lon))
            except (ValueError, TypeError):
                continue
        return coords if coords else None
