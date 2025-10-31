
class RecordThread:
    '''A class representing a thread record with ID and name.
    Attributes
    ----------
    id : int
        The thread ID
    name : str
        The thread name
    '''

    def __init__(self, id_, name):
        '''Initialize a RecordThread instance.
        Parameters
        ----------
        id_ : int
            The thread ID
        name : str
            The thread name
        '''
        self.id = id_
        self.name = name

    def __repr__(self):
        '''Return string representation of RecordThread.
        Returns
        -------
        str
            Formatted string with id and name
        '''
        return f"RecordThread(id={self.id}, name='{self.name}')"

    def __format__(self, spec):
        '''Format the RecordThread instance.
        Parameters
        ----------
        spec : str
            Format specification
        Returns
        -------
        str
            Formatted ID according to specification
        '''
        return format(self.id, spec)


# Example usage:
def main():
    thread = RecordThread(123, "Main Thread")
    print(repr(thread))
    print(f"{thread:x}")
    print(f"{thread:08d}")


if __name__ == "__main__":
    main()
