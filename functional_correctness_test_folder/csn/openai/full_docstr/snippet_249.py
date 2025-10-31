
import sys
from string import Template as StrTemplate


class Template:
    '''Provide tool to manage templates
    '''

    def __init__(self):
        '''Class instantiation
        '''
        # No internal state needed for this simple implementation
        pass

    def render(self, sources, config, out=sys.stdout):
        '''Render the documentation as defined in config Object

        Parameters
        ----------
        sources : dict
            Mapping of template names to template strings.
        config : dict or str
            If a dict, it must contain:
                - 'template': name of the template in `sources`
                - 'variables': dict of variables to substitute
            If a str, it is treated as the template name with no variables.
        out : file-like, optional
            Destination to write the rendered output. Defaults to sys.stdout.

        Returns
        -------
        str
            The rendered string.
        '''
        # Resolve template name and variables
        if isinstance(config, dict):
            template_name = config.get('template')
            variables = config.get('variables', {})
        elif isinstance(config, str):
            template_name = config
            variables = {}
        else:
            raise TypeError('config must be a dict or a str')

        if template_name is None:
            raise ValueError('config must specify a template name')

        # Retrieve the template string
        try:
            template_str = sources[template_name]
        except KeyError:
            raise KeyError(f'Template "{template_name}" not found in sources')

        # Perform substitution
        try:
            # Prefer str.format if variables are provided
            if variables:
                rendered = template_str.format(**variables)
            else:
                # Fallback to string.Template for simple ${var} syntax
                rendered = StrTemplate(template_str).substitute()
        except Exception as exc:
            raise RuntimeError(
                f'Error rendering template "{template_name}": {exc}')

        # Write to the output stream
        out.write(rendered)
        return rendered
