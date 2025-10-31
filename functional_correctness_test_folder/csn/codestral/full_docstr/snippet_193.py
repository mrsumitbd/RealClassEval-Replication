
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
        flags_text = []
        if hasattr(self, 'flags'):
            for i in range(32):
                if self.flags & (1 << i):
                    flags_text.append(f'CKF_{i}')
        return flags_text

    def state2text(self):
        '''
        Dummy method. Will be overwriden if necessary
        '''
        pass

    def to_dict(self):
        '''
        convert the fields of the object into a dictionnary
        '''
        obj_dict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, (int, float, str, bool)):
                obj_dict[key] = value
            elif hasattr(value, 'to_dict'):
                obj_dict[key] = value.to_dict()
            else:
                obj_dict[key] = str(value)
        return obj_dict

    def __str__(self):
        '''
        text representation of the object
        '''
        return str(self.to_dict())
