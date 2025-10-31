
class TorConfigType:
    '''
    Base class for all configuration types, which function as parsers
    and un-parsers.
    '''

    def parse(self, s):
        '''
        Given the string s, this should return a parsed representation
        of it.
        '''
        return s

    def validate(self, s, instance, name):
        '''
        If s is not a valid type for this object, an exception should
        be thrown. The validated object should be returned.
        '''
        # By default, accept any string
        if not isinstance(s, str):
            raise ValueError(
                f"Value for {name} must be a string, got {type(s).__name__}")
        return s
