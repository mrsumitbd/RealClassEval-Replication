
import random


class Sampleable:

    def __init__(self, data=None):
        """
        Initialize the Sampleable class.

        Args:
        data (list): A list of data to sample from. Defaults to None.
        """
        self.data = data if data is not None else []

    def get_sample(self, size=1, replacement=False):
        """
        Get a random sample from the data.

        Args:
        size (int): The size of the sample. Defaults to 1.
        replacement (bool): Whether to sample with replacement. Defaults to False.

        Returns:
        list: A list of sampled data.
        """
        if not self.data:
            return []
        return random.choices(self.data, k=size) if replacement else random.sample(self.data, min(size, len(self.data)))

    def get_default_sample(self):
        """
        Get a default sample from the data.

        Returns:
        The first element of the data if it exists, otherwise None.
        """
        return self.data[0] if self.data else None


# Example usage:
if __name__ == "__main__":
    sampleable = Sampleable([1, 2, 3, 4, 5])
    print(sampleable.get_sample(3))  # Sample without replacement
    # Sample with replacement
    print(sampleable.get_sample(3, replacement=True))
    print(sampleable.get_default_sample())  # Get the default sample
