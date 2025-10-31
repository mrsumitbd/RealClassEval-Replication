
import sys
from jinja2 import Template as JinjaTemplate


class Template:

    def __init__(self, template_str):
        """
        Initialize the Template class.

        Args:
        template_str (str): A string representing the template.
        """
        self.template = JinjaTemplate(template_str)

    def render(self, sources, config, out=sys.stdout):
        """
        Render the template with the given sources and config.

        Args:
        sources (dict): A dictionary containing the sources to be used in the template.
        config (dict): A dictionary containing the configuration to be used in the template.
        out (file-like object): The output stream where the rendered template will be written. Defaults to sys.stdout.
        """
        # Combine sources and config into a single dictionary
        data = {**sources, **config}

        # Render the template with the combined data
        rendered_template = self.template.render(data)

        # Write the rendered template to the output stream
        out.write(rendered_template)


# Example usage:
if __name__ == "__main__":
    template_str = "Hello, {{ name }}! Your age is {{ age }}."
    template = Template(template_str)

    sources = {"name": "John"}
    config = {"age": 30}

    template.render(sources, config)
