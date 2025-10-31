
import sys


class Template:

    def __init__(self):
        '''Class instantiation
        '''
        self.data = {}

    def render(self, sources, config, out=sys.stdout):
        '''Render the documentation as defined in config Object
        '''
        for source in sources:
            with open(source, 'r') as file:
                self.data[source] = file.read()

        for key, value in config.items():
            if key in self.data:
                self.data[key] = self.data[key].format(**value)

        for content in self.data.values():
            out.write(content)
