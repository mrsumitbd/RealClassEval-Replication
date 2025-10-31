
class RecordFile:
    '''A class representing a file record with name and path.
    Attributes
    ----------
    name : str
        The name of the file
    path : str
        The path to the file
    '''

    def __init__(self, name, path):
        '''Initialize a RecordFile instance.
        Parameters
        ----------
        name : str
            The name of the file
        path : str
            The path to the file
        '''
        self.name = name
        self.path = path

    def __repr__(self):
        '''Return string representation of RecordFile.
        Returns
        -------
        str
            Formatted string with name and path
        '''
        return f"RecordFile(name='{self.name}', path='{self.path}')"

    def __format__(self, spec):
        '''Format the RecordFile instance.
        Parameters
        ----------
        spec : str
            Format specification
        Returns
        -------
        str
            Formatted name according to specification
        '''
        return format(self.name, spec)


# Example usage:
def main():
    file_record = RecordFile("example.txt", "/home/user/documents")
    print(repr(file_record))
    print(f"{file_record}")
    print(f"{file_record:.5}")


if __name__ == "__main__":
    main()
