
class TorConfigType:
    '''
    Base class for all configuration types, which function as parsers
    and un-parsers.
    '''

    def parse(self, s):
        # By default, just return the string as is
        return s

    def validate(self, s, instance, name):
        # By default, accept any value (no validation)
        return True
