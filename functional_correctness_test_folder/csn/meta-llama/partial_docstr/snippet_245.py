
class Sampleable:
    '''Element who can provide samples
    '''

    def __init__(self, default_value=None, samples=None):
        self.default_value = default_value
        self.samples = samples if samples is not None else []

    def get_sample(self):
        '''Return a sample for the element
        '''
        if self.samples:
            return self.samples[0]  # Return the first sample
        else:
            return self.get_default_sample()

    def get_default_sample(self):
        '''Return default value for the element
        '''
        return self.default_value


# Example usage:
if __name__ == "__main__":
    sampleable = Sampleable(default_value=10, samples=[5, 7, 9])
    print(sampleable.get_sample())  # Output: 5
    print(sampleable.get_default_sample())  # Output: 10

    sampleable_no_samples = Sampleable(default_value=10)
    print(sampleable_no_samples.get_sample())  # Output: 10
    print(sampleable_no_samples.get_default_sample())  # Output: 10
