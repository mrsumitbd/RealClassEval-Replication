
import sys
from jinja2 import Template as JinjaTemplate


class Template:

    def __init__(self, template_str):
        '''Class instantiation
        '''
        self.template = JinjaTemplate(template_str)

    def render(self, sources, config, out=sys.stdout):
        '''Render the documentation as defined in config Object
        '''
        rendered_template = self.template.render(
            sources=sources, config=config)
        out.write(rendered_template)
