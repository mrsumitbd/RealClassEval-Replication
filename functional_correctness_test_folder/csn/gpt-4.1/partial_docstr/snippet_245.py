
import random


class Sampleable:
    '''Element who can provide samples
    '''

    def __init__(self):
        self.samples = [1, 2, 3, 4, 5]
        self.default = 0

    def get_sample(self):
        '''Return the a sample for the element
        '''
        return random.choice(self.samples)

    def get_default_sample(self):
        '''Return default value for the element
        '''
        return self.default
