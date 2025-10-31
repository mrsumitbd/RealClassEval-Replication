
from abc import ABC, abstractmethod


class Geometry(ABC):
    '''
    Abstract parent class for geotypes
    '''
    @abstractmethod
    def geojson(self):
        pass

    @abstractmethod
    def to_dict(self):
        '''
        Returns a dict representation of this geotype
        :return: dict
        '''
        pass
