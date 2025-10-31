
import json


class Geometry:
    def __init__(self, geometry_type, coordinates):
        """
        Initialize a Geometry object.

        Args:
            geometry_type (str): The type of geometry (e.g., 'Point', 'LineString', 'Polygon').
            coordinates (list): The coordinates of the geometry.
        """
        self.geometry_type = geometry_type
        self.coordinates = coordinates

    def geojson(self):
        """
        Return the geometry as a GeoJSON string.

        Returns:
            str: The GeoJSON representation of the geometry.
        """
        geojson_dict = self.to_dict()
        return json.dumps(geojson_dict)

    def to_dict(self):
        """
        Return the geometry as a dictionary.

        Returns:
            dict: The dictionary representation of the geometry.
        """
        return {
            'type': self.geometry_type,
            'coordinates': self.coordinates
        }


# Example usage:
if __name__ == "__main__":
    point = Geometry('Point', [12.5, 34.7])
    print(point.geojson())
    print(point.to_dict())

    linestring = Geometry('LineString', [[12.5, 34.7], [13.2, 35.1]])
    print(linestring.geojson())
    print(linestring.to_dict())

    polygon = Geometry(
        'Polygon', [[[12.5, 34.7], [13.2, 35.1], [12.8, 35.3], [12.5, 34.7]]])
    print(polygon.geojson())
    print(polygon.to_dict())
