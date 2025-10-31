
class Sampleable:
    '''Element who can provide samples
    '''

    def __init__(self, default_value=None):
        self.default_value = default_value

    def get_sample(self):
        '''Return the a sample for the element
        '''
        # This is a placeholder implementation. In a real scenario, this method should return a meaningful sample.
        return self.default_value

    def get_default_sample(self):
        '''Return default value for the element
        '''
        return self.default_value
