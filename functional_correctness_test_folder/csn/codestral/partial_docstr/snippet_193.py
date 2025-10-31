
class CkClass:

    def flags2text(self):
        pass

    def state2text(self):
        '''
        Dummy method. Will be overwriden if necessary
        '''
        pass

    def to_dict(self):
        '''
        convert the fields of the object into a dictionnary
        '''
        return self.__dict__

    def __str__(self):
        '''
        text representation of the object
        '''
        return str(self.__dict__)
