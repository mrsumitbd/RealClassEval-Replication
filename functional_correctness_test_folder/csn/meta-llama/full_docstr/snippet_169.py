
class Cursor:
    '''Interface that abstracts the cursor object returned from databases.'''

    def __init__(self, data):
        '''Declare a new cursor to iterate over runs.'''
        self.data = data
        self.index = 0

    def count(self):
        '''Return the number of items in this cursor.'''
        return len(self.data)

    def __iter__(self):
        '''Iterate over elements.'''
        return self

    def __next__(self):
        if self.index < len(self.data):
            result = self.data[self.index]
            self.index += 1
            return result
        raise StopIteration


# Example usage:
if __name__ == "__main__":
    data = [1, 2, 3, 4, 5]
    cursor = Cursor(data)
    print("Count:", cursor.count())
    for item in cursor:
        print(item)
