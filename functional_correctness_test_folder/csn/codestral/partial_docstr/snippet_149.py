
class TorConfigType:
    '''
    Base class for all configuration types, which function as parsers
    and un-parsers.
    '''

    def parse(self, s):
        pass

    def validate(self, s, instance, name):
        pass
