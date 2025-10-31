
class CkClass:

    def __init__(self, flags=None, state=None, **kwargs):
        self.flags = flags
        self.state = state
        for key, value in kwargs.items():
            setattr(self, key, value)

    def flags2text(self):
        flag_mapping = {
            0: 'None',
            1: 'Flag1',
            2: 'Flag2',
            # Add more flag mappings as needed
        }
        return flag_mapping.get(self.flags, 'Unknown')

    def state2text(self):
        '''
        Dummy method. Will be overwritten if necessary
        '''
        state_mapping = {
            0: 'Unknown',
            # Add more state mappings as needed
        }
        return state_mapping.get(self.state, 'Unknown')

    def to_dict(self):
        '''
        convert the fields of the object into a dictionary
        '''
        obj_dict = self.__dict__.copy()
        return obj_dict

    def __str__(self):
        '''
        text representation of the object
        '''
        obj_str = f"CkClass - Flags: {self.flags2text()}, State: {self.state2text()}\n"
        for key, value in self.to_dict().items():
            if key not in ['flags', 'state']:
                obj_str += f"{key}: {value}\n"
        return obj_str.strip()
