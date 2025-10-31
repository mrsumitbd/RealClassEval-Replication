import json

class LocationCollectionUtils:

    @classmethod
    def extract_coords_key(cls, item):
        try:
            coord1, coord2 = (float(item[0]), float(item[1]))
        except IndexError:
            raise ValueError('Two values are required for a coordinate pair')
        except ValueError:
            raise ValueError('Only float or float-coercable values can be passed')
        return '{0},{1}'.format(coord1, coord2)

    @classmethod
    def get_lookup_key(cls, item):
        if isinstance(item, tuple):
            key = cls.extract_coords_key(item)
        elif isinstance(item, dict):
            key = json.dumps(item)
        else:
            key = item
        return key