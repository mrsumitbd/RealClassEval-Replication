
import sys


class Template:

    def __init__(self):
        '''Class instantiation
        '''
        pass

    def render(self, sources, config, out=sys.stdout):
        '''Render the documentation as defined in config Object
        '''
        title = getattr(config, 'title', 'Documentation')
        header = getattr(config, 'header', '')
        footer = getattr(config, 'footer', '')
        section_order = getattr(config, 'section_order', None)

        print(f"# {title}", file=out)
        if header:
            print(header, file=out)
            print(file=out)

        if section_order is None:
            section_order = list(sources.keys())
        for section in section_order:
            if section in sources:
                print(f"## {section}", file=out)
                print(sources[section], file=out)
                print(file=out)

        if footer:
            print(footer, file=out)
