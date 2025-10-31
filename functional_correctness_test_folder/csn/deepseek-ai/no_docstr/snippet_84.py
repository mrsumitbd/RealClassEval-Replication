
class Scheme:

    def __init__(self, title):
        self.title = title
        self.arguments = []

    def add_argument(self, arg):
        self.arguments.append(arg)

    def to_xml(self):
        xml_parts = []
        xml_parts.append(f'<scheme title="{self.title}">')
        for arg in self.arguments:
            xml_parts.append(f'    <argument>{arg}</argument>')
        xml_parts.append('</scheme>')
        return '\n'.join(xml_parts)
