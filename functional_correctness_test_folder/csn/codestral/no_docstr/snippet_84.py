
class Scheme:

    def __init__(self, title):
        self.title = title
        self.arguments = []

    def add_argument(self, arg):
        self.arguments.append(arg)

    def to_xml(self):
        xml = f'<scheme title="{self.title}">\n'
        for arg in self.arguments:
            xml += f'  <argument>{arg}</argument>\n'
        xml += '</scheme>'
        return xml
