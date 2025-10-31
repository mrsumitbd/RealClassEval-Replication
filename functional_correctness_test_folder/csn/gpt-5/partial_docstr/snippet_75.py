import abc
import json
from typing import Dict, Any


class Geometry(metaclass=abc.ABCMeta):
    '''
    Abstract parent class for geotypes
    '''

    def geojson(self) -> str:
        return json.dumps(self.to_dict(), separators=(',', ':'))

    @abc.abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        '''
        Returns a dict representation of this geotype
        :return: dict
        '''
        raise NotImplementedError
