
class TorConfigType:
    '''
    Base class for all configuration types, which function as parsers
    and un-parsers.
    '''

    def parse(self, s):
        raise NotImplementedError("Subclasses must implement this method")

    def validate(self, s, instance, name):
        raise NotImplementedError("Subclasses must implement this method")
