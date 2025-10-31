
import sys


class Template:

    def __init__(self):
        pass

    def render(self, sources, config, out=sys.stdout):
        for source in sources:
            text = source
            for key, value in config.items():
                placeholder = '{' + str(key) + '}'
                text = text.replace(placeholder, str(value))
            print(text, file=out)
