class Capability:

    def __init__(self, uri):
        self.parameters = {}
        if '?' in uri:
            id_, pars = uri.split('?')
            self.parse_pars(pars)
        else:
            id_ = uri
        self.id = id_

    def parse_pars(self, pars):
        for p in pars.split('&'):
            name, value = p.split('=')
            self.parameters[name] = value