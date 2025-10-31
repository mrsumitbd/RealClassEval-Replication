import yaml

class Style:

    def __init__(self, header=None, footer=None, tokens=None, events=None, replaces=None):
        self.header = header
        self.footer = footer
        self.replaces = replaces
        self.substitutions = {}
        for domain, Class in [(tokens, 'Token'), (events, 'Event')]:
            if not domain:
                continue
            for key in domain:
                name = ''.join([part.capitalize() for part in key.split('-')])
                cls = getattr(yaml, '%s%s' % (name, Class))
                value = domain[key]
                if not value:
                    continue
                start = value.get('start')
                end = value.get('end')
                if start:
                    self.substitutions[cls, -1] = start
                if end:
                    self.substitutions[cls, +1] = end

    def __setstate__(self, state):
        self.__init__(**state)