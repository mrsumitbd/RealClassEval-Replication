
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
        flag_map = {
            0x0001: 'CKF_HW',
            0x0002: 'CKF_ENCRYPT',
            0x0004: 'CKF_DECRYPT',
            0x0008: 'CKF_DIGEST',
            0x0010: 'CKF_SIGN',
            0x0020: 'CKF_SIGN_RECOVER',
            0x0040: 'CKF_VERIFY',
            0x0080: 'CKF_VERIFY_RECOVER',
            0x0100: 'CKF_GENERATE',
            0x0200: 'CKF_GENERATE_KEY_PAIR',
            0x0400: 'CKF_WRAP',
            0x0800: 'CKF_UNWRAP',
            0x1000: 'CKF_DERIVE',
            0x2000: 'CKF_LOCAL',
            0x4000: 'CKF_MODIFIABLE',
            0x8000: 'CKF_EC_F_P',
            0x10000: 'CKF_EC_F_2M',
            0x20000: 'CKF_EC_ECPARAMETERS',
            0x40000: 'CKF_EC_NAMEDCURVE',
            0x80000: 'CKF_EC_UNCOMPRESS',
            0x100000: 'CKF_EC_COMPRESS',
        }
        return [flag_map[flag] for flag in flag_map if self.flags & flag]

    def state2text(self):
        '''
        Dummy method. Will be overwriden if necessary
        '''
        return "State not defined"

    def to_dict(self):
        '''
        convert the fields of the object into a dictionary
        '''
        return {attr: getattr(self, attr) for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")}

    def __str__(self):
        '''
        text representation of the object
        '''
        return str(self.to_dict())
