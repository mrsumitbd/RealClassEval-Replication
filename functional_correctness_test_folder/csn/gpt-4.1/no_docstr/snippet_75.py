
class Geometry:

    def geojson(self):
        d = self.to_dict()
        d['type'] = self.__class__.__name__
        return d

    def to_dict(self):
        return {'type': self.__class__.__name__}
