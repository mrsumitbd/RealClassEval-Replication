
class Geometry:

    def geojson(self):
        return {
            "type": "Geometry",
            "coordinates": []
        }

    def to_dict(self):
        return {
            "class": "Geometry",
            "properties": {}
        }
