class Bunch:

    def __init__(self, kwds):
        tmp = {}
        for key, value in kwds.iteritems():
            tmp[key] = Bunch(value) if isinstance(value, dict) else value
        self.__dict__.update(tmp)

    def get_attributes(self):
        return self.__dict__.keys()