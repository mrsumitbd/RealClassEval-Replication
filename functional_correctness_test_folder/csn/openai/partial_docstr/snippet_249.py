
import sys
import string
import os


class Template:
    def __init__(self):
        '''Class instantiation'''
        pass

    def render(self, sources, config, out=sys.stdout):
        '''Render the documentation as defined in config Object'''
        # Determine template string from config
        tmpl_str = None
        tmpl_file = None

        if isinstance(config, dict):
            tmpl_str = config.get('template')
            tmpl_file = config.get('template_file')
        else:
            tmpl_str = getattr(config, 'template', None)
            tmpl_file = getattr(config, 'template_file', None)

        if tmpl_file:
            if not os.path.isfile(tmpl_file):
                raise FileNotFoundError(
                    f"Template file not found: {tmpl_file}")
            with open(tmpl_file, 'r', encoding='utf-8') as f:
                tmpl_str = f.read()

        if tmpl_str is None:
            raise ValueError("No template provided in config")

        tmpl = string.Template(tmpl_str)

        try:
            rendered = tmpl.substitute(sources)
        except KeyError as e:
            raise KeyError(f"Missing key in sources for template: {e}") from e

        out.write(rendered)
