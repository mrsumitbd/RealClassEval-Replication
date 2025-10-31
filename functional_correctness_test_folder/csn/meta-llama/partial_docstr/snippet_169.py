
class Cursor:

    def __init__(self, data=None):
        """Initialize the Cursor object.

        Args:
            data (list, optional): The data to be stored in the cursor. Defaults to None.
        """
        if data is None:
            data = []
        self.data = data
        self.index = 0

    def count(self):
        '''Return the number of items in this cursor.'''
        return len(self.data)

    def __iter__(self):
        '''Return the iterator object itself.'''
        return self

    def __next__(self):
        '''Return the next item from the container.'''
        if self.index < len(self.data):
            result = self.data[self.index]
            self.index += 1
            return result
        else:
            self.index = 0  # Reset the index for future iterations
            raise StopIteration


# Example usage:
if __name__ == "__main__":
    cursor = Cursor([1, 2, 3, 4, 5])
    print("Count:", cursor.count())  # Output: Count: 5

    print("Iterating over the cursor:")
    for item in cursor:
        print(item)

    # Demonstrating that the cursor can be iterated over multiple times
    print("Iterating over the cursor again:")
    for item in cursor:
        print(item)
