
from abc import ABC, abstractmethod


class Geometry(ABC):
    """
    Abstract parent class for geotypes.
    """

    @abstractmethod
    def geojson(self):
        """
        Return a GeoJSON representation of the geometry.
        """
        pass

    @abstractmethod
    def to_dict(self):
        """
        Return a dictionary representation of this geotype.
        """
        pass
