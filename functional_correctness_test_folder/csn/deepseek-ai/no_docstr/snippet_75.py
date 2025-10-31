
class Geometry:

    def geojson(self):
        raise NotImplementedError("Subclasses must implement this method")

    def to_dict(self):
        raise NotImplementedError("Subclasses must implement this method")
