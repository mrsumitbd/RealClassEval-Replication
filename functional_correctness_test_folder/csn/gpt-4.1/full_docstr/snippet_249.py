
import sys
import string


class Template:
    '''Provide tool to managed templates
    '''

    def __init__(self):
        '''Class instantiation
        '''
        pass

    def render(self, sources, config, out=sys.stdout):
        '''Render the documentation as defined in config Object
        '''
        # config is expected to be a dict with at least a 'template' key
        # sources is a dict of variables to substitute
        template_str = config.get('template', '')
        # Use string.Template for substitution
        tmpl = string.Template(template_str)
        rendered = tmpl.safe_substitute(sources)
        print(rendered, file=out)
