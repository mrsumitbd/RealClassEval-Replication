
from abc import ABC, abstractmethod
import json


class Geometry(ABC):
    """
    Abstract parent class for geotypes.
    """

    @abstractmethod
    def geojson(self) -> str:
        """
        Returns a GeoJSON string representation of this geotype,
        compliant to RFC 7946 (https://tools.ietf.org/html/rfc7946).

        :return: str
        """
        raise NotImplementedError("Subclasses must implement geojson()")

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Returns a dict representation of this geotype.

        :return: dict
        """
        raise NotImplementedError("Subclasses must implement to_dict()")
