import json


class Geometry:
    '''
    Abstract parent class for geotypes
    '''

    def geojson(self):
        '''
        Returns a GeoJSON string representation of this geotype, compliant to
        RFC 7946 (https://tools.ietf.org/html/rfc7946)
        :return: str
        '''
        return json.dumps(self.to_dict(), ensure_ascii=False, separators=(",", ":"))

    def to_dict(self):
        '''
        Returns a dict representation of this geotype
        :return: dict
        '''
        raise NotImplementedError("Subclasses must implement to_dict()")
