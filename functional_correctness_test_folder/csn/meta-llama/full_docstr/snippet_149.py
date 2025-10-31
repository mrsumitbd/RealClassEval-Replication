
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
        raise NotImplementedError("Subclass must implement parse method")

    def validate(self, s, instance, name):
        '''
        If s is not a valid type for this object, an exception should
        be thrown. The validated object should be returned.
        '''
        raise NotImplementedError("Subclass must implement validate method")
