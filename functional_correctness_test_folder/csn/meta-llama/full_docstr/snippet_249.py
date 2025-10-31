
import sys
from jinja2 import Template as JinjaTemplate
import yaml


class Template:
    '''Provide tool to managed templates
    '''

    def __init__(self):
        '''Class instantiation
        '''
        self.jinja_template = None

    def render(self, sources, config, out=sys.stdout):
        '''Render the documentation as defined in config Object
        '''
        try:
            with open(config['template'], 'r') as file:
                self.jinja_template = JinjaTemplate(file.read())
        except FileNotFoundError:
            print(f"Template file {config['template']} not found.")
            return

        data = {}
        for source in sources:
            try:
                with open(source, 'r') as file:
                    data[source] = yaml.safe_load(file)
            except FileNotFoundError:
                print(f"Source file {source} not found.")
                return
            except yaml.YAMLError as e:
                print(f"Failed to parse {source}: {e}")
                return

        rendered_template = self.jinja_template.render(
            data=data, config=config)
        out.write(rendered_template)


# Example usage:
if __name__ == "__main__":
    template = Template()
    sources = ['data.yaml']
    config = {'template': 'template.j2'}
    template.render(sources, config)
