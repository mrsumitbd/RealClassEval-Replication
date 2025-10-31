
class CkClass:

    def flags2text(self):
        return ""

    def state2text(self):
        '''
        Dummy method. Will be overwriden if necessary
        '''
        return ""

    def to_dict(self):
        '''
        convert the fields of the object into a dictionnary
        '''
        return vars(self)

    def __str__(self):
        '''
        text representation of the object
        '''
        return str(self.to_dict())
