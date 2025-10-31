
class CkClass:
    '''
    Base class for CK_* classes
    '''

    def __init__(self, flags, state):
        self.flags = flags
        self.state = state

    def flags2text(self):
        '''
        parse the `self.flags` field and create a list of `CKF_*` strings
        corresponding to bits set in flags
        :return: a list of strings
        :rtype: list
        '''
        flag_dict = {
            0x00000001: 'CKF_TOKEN_PRESENT',
            0x00000002: 'CKF_REMOVABLE_DEVICE',
            0x00000004: 'CKF_HW_SLOT',
            # Add more flag definitions as needed
        }
        return [flag_name for flag_value, flag_name in flag_dict.items() if self.flags & flag_value]

    def state2text(self):
        '''
        Dummy method. Will be overwritten if necessary
        '''
        return 'Unknown'

    def to_dict(self):
        '''
        convert the fields of the object into a dictionary
        '''
        return {
            'flags': self.flags,
            'flags_text': self.flags2text(),
            'state': self.state,
            'state_text': self.state2text(),
        }

    def __str__(self):
        '''
        text representation of the object
        '''
        output = f'Flags: {self.flags} ({", ".join(self.flags2text())})\n'
        output += f'State: {self.state} ({self.state2text()})'
        return output
