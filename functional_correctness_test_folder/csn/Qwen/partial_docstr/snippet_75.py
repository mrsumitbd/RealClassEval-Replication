
class Geometry:
    '''
    Abstract parent class for geotypes
    '''

    def geojson(self):
        raise NotImplementedError(
            "This method should be overridden by subclasses")

    def to_dict(self):
        '''
        Returns a dict representation of this geotype
        :return: dict
        '''
        raise NotImplementedError(
            "This method should be overridden by subclasses")
