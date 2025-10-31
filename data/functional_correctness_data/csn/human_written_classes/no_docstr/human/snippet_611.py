class AbstractConfigurationLoader:

    def __repr__(self):
        raise NotImplementedError()

    def __contains__(self, item):
        raise NotImplementedError()

    def __getitem__(self, item):
        raise NotImplementedError()

    def check(self):
        return True