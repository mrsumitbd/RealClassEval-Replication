
import sys


class Template:

    def __init__(self):
        self.template_data = ""

    def render(self, sources, config, out=sys.stdout):
        for source in sources:
            with open(source, 'r') as file:
                self.template_data += file.read()

        for key, value in config.items():
            self.template_data = self.template_data.replace(
                f"{{{key}}}", str(value))

        out.write(self.template_data)
