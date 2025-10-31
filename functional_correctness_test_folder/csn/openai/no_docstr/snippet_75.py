
class Geometry:
    def __init__(self, geom_type, coordinates):
        """
        Initialize a Geometry instance.

        Parameters
        ----------
        geom_type : str
            The type of the geometry (e.g., "Point", "LineString", "Polygon").
        coordinates : list or tuple
            The coordinates of the geometry. The structure depends on the geometry type.
        """
        self.type = geom_type
        self.coordinates = coordinates

    def geojson(self):
        """
        Return a GeoJSON representation of the geometry.

        Returns
        -------
        dict
            A dictionary following the GeoJSON specification.
        """
        return {"type": self.type, "coordinates": self.coordinates}

    def to_dict(self):
        """
        Return a plain dictionary representation of the geometry.

        Returns
        -------
        dict
            A dictionary containing the geometry type and coordinates.
        """
        return {"type": self.type, "coordinates": self.coordinates}
