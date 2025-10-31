
import json
from abc import ABC, abstractmethod


class Geometry(ABC):
    '''
    Abstract parent class for geotypes
    '''

    @abstractmethod
    def to_dict(self):
        '''
        Returns a dict representation of this geotype
        :return: dict
        '''
        pass

    def geojson(self):
        '''
        Returns a GeoJSON string representation of this geotype, compliant to
        RFC 7946 (https://tools.ietf.org/html/rfc7946)
        :return: str
        '''
        return json.dumps(self.to_dict())
