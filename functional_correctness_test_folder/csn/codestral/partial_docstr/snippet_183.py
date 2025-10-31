
class Reader:
    '''
    The reader provides integration with cache.
    @ivar options: An options object.
    @type options: I{Options}
    '''

    def __init__(self, options):
        self.options = options

    def mangle(self, name, x):
        return f"{name}_{x}"
