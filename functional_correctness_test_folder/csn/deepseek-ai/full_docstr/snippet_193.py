
class CkClass:
    '''
    Base class for CK_* classes
    '''

    def flags2text(self):
        '''
        parse the `self.flags` field and create a list of `CKF_*` strings
        corresponding to bits set in flags
        :return: a list of strings
        :rtype: list
        '''
        if not hasattr(self, 'flags'):
            return []
        flags = self.flags
        flag_names = []
        for name in dir(self):
            if name.startswith('CKF_'):
                flag_value = getattr(self, name)
                if flags & flag_value:
                    flag_names.append(name)
        return flag_names

    def state2text(self):
        '''
        Dummy method. Will be overwriden if necessary
        '''
        pass

    def to_dict(self):
        '''
        convert the fields of the object into a dictionnary
        '''
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                result[key] = value
        return result

    def __str__(self):
        '''
        text representation of the object
        '''
        return str(self.to_dict())
