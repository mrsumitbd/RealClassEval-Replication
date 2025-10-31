
class Sampleable:
    '''Element who can provide samples
    '''

    def __init__(self):
        '''Class instantiation
        '''
        self.samples = []
        self.default_sample = None

    def get_sample(self):
        '''Return the a sample for the element
        '''
        if self.samples:
            return self.samples[0]
        return self.get_default_sample()

    def get_default_sample(self):
        '''Return default value for the element
        '''
        return self.default_sample
