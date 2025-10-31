
class Geometry:
    '''
    Abstract parent class for geotypes
    '''

    def geojson(self):
        pass

    def to_dict(self):
        '''
        Returns a dict representation of this geotype
        :return: dict
        '''
        pass
