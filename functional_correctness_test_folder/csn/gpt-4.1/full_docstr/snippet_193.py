
import re


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
        flags_value = self.flags
        # Find all CKF_* attributes in the class or its bases
        flag_names = []
        for cls in self.__class__.__mro__:
            for name, value in cls.__dict__.items():
                if re.match(r'^CKF_', name) and isinstance(value, int):
                    if flags_value & value:
                        flag_names.append(name)
        return sorted(set(flag_names))

    def state2text(self):
        '''
        Dummy method. Will be overwriden if necessary
        '''
        return None

    def to_dict(self):
        '''
        convert the fields of the object into a dictionnary
        '''
        d = {}
        for k, v in self.__dict__.items():
            d[k] = v
        return d

    def __str__(self):
        '''
        text representation of the object
        '''
        fields = ', '.join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({fields})"
