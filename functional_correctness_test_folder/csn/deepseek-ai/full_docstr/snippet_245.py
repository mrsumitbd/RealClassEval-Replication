
class Sampleable:
    '''Element who can provide samples
    '''

    def __init__(self):
        '''Class instantiation
        '''
        pass

    def get_sample(self):
        '''Return the a sample for the element
        '''
        raise NotImplementedError("Subclasses must implement get_sample()")

    def get_default_sample(self):
        '''Return default value for the element
        '''
        raise NotImplementedError(
            "Subclasses must implement get_default_sample()")
