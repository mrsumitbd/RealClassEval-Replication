
import random


class Sampleable:
    '''Element who can provide samples
    '''

    def __init__(self, default_value=None, sample_generator=None):
        '''Class instantiation
        '''
        self.default_value = default_value
        self.sample_generator = sample_generator

    def get_sample(self):
        '''Return the a sample for the element
        '''
        if self.sample_generator is not None:
            return next(self.sample_generator)
        else:
            return self.default_value

    def get_default_sample(self):
        '''Return default value for the element
        '''
        return self.default_value


# Example usage:


def generate_random_samples():
    while True:
        yield random.randint(0, 100)


sampleable = Sampleable(
    default_value=50, sample_generator=generate_random_samples())
print(sampleable.get_sample())  # prints a random number between 0 and 100
print(sampleable.get_default_sample())  # prints 50

sampleable_without_generator = Sampleable(default_value=50)
print(sampleable_without_generator.get_sample())  # prints 50
print(sampleable_without_generator.get_default_sample())  # prints 50
