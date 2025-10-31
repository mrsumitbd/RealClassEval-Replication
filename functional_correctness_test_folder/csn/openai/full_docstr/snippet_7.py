class RecordLevel:
    '''A class representing the logging level record with name, number and icon.
    Attributes
    ----------
    icon : str
        The icon representing the log level
    name : str
        The name of the log level
    no : int
        The numeric value of the log level
    '''

    def __init__(self, name, no, icon):
        '''Initialize a RecordLevel instance.
        Parameters
        ----------
        name : str
            The name of the log level
        no : int
            The numeric value of the log level
        icon : str
            The icon representing the log level
        '''
        self.name = name
        self.no = no
        self.icon = icon

    def __repr__(self):
        '''Return string representation of RecordLevel.
        Returns
        -------
        str
            Formatted string with name, number and icon
        '''
        return f"<RecordLevel name={self.name!r} no={self.no} icon={self.icon!r}>"

    def __format__(self, spec):
        '''Format the RecordLevel instance.
        Parameters
        ----------
        spec : str
            Format specification
        Returns
        -------
        str
            Formatted name according to specification
        '''
        if not spec:
            return self.name
        # Simple spec handling: 'n' -> name, 'i' -> icon, 'o' -> number
        if spec == 'n':
            return self.name
        if spec == 'i':
            return self.icon
        if spec == 'o':
            return str(self.no)
        # If spec contains multiple tokens, join them with spaces
        parts = []
        for token in spec.split(','):
            token = token.strip()
            if token == 'n':
                parts.append(self.name)
            elif token == 'i':
                parts.append(self.icon)
            elif token == 'o':
                parts.append(str(self.no))
            else:
                parts.append(self.name)
        return ' '.join(parts)
