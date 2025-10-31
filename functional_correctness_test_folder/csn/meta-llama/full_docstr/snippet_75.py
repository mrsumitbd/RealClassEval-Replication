
import json
from abc import ABC, abstractmethod


class Geometry(ABC):
    '''
    Abstract parent class for geotypes
    '''

    @abstractmethod
    def geojson(self):
        '''
        Returns a GeoJSON string representation of this geotype, compliant to
        RFC 7946 (https://tools.ietf.org/html/rfc7946)
        :return: str
        '''
        pass

    @abstractmethod
    def to_dict(self):
        '''
        Returns a dict representation of this geotype
        :return: dict
        '''
        pass

    def __str__(self):
        return self.geojson()

    def __repr__(self):
        return f'{self.__class__.__name__}({json.dumps(self.to_dict())})'
