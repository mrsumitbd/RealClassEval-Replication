
class Geometry:
    '''
    Abstract parent class for geotypes
    '''

    def geojson(self):
        '''
        Returns a GeoJSON representation of this geotype
        :return: dict
        '''
        raise NotImplementedError("Subclasses must implement geojson()")

    def to_dict(self):
        '''
        Returns a dict representation of this geotype
        :return: dict
        '''
        raise NotImplementedError("Subclasses must implement to_dict()")
