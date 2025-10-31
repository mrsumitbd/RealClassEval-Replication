
import sys


class Template:
    '''Provide tool to managed templates
    '''

    def __init__(self):
        '''Class instantiation
        '''
        self.templates = {}

    def render(self, sources, config, out=sys.stdout):
        '''Render the documentation as defined in config Object
        '''
        for source in sources:
            template_name = source.get('template')
            if template_name in self.templates:
                template = self.templates[template_name]
                rendered_content = template.format(**config)
                out.write(rendered_content)
            else:
                raise ValueError(f"Template {template_name} not found.")

    def add_template(self, name, content):
        '''Add a new template to the manager
        '''
        self.templates[name] = content
