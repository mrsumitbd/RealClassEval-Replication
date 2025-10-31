
class NestedDummyClass:
    class Inner:
        def __init__(self):
            self.value = 42

    def run(self):
        '''Do nothing.'''
        pass

    @property
    def prop(self):
        return self.Inner()
