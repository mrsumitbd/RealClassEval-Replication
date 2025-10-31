class Sampleable:
    '''Element who can provide samples
    '''

    def __init__(self, sample=None, default=None, sampler=None):
        '''Class instantiation
        '''
        self._sample = sample
        self._default_sample = default
        self._sampler = sampler

    def get_sample(self):
        '''Return the a sample for the element
        '''
        if callable(self._sampler):
            return self._sampler()
        if self._sample is not None:
            return self._sample
        return self.get_default_sample()

    def get_default_sample(self):
        '''Return default value for the element
        '''
        return self._default_sample
