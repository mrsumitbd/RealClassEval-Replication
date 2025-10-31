
import xml.etree.ElementTree as ET


class Scheme:
    def __init__(self, title):
        self.title = title
        self.arguments = []

    def add_argument(self, arg):
        """Add an argument to the scheme."""
        self.arguments.append(arg)

    def to_xml(self):
        """Return an XML string representation of the scheme."""
        root = ET.Element('scheme', attrib={'title': self.title})
        for arg in self.arguments:
            arg_el = ET.SubElement(root, 'argument')
            arg_el.text = str(arg)
        return ET.tostring(root, encoding='unicode')
