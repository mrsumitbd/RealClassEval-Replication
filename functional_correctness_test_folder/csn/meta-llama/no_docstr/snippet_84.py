
import xml.etree.ElementTree as ET


class Scheme:

    def __init__(self, title):
        self.title = title
        self.arguments = []

    def add_argument(self, arg):
        self.arguments.append(arg)

    def to_xml(self):
        root = ET.Element("scheme")
        title_element = ET.SubElement(root, "title")
        title_element.text = self.title

        args_element = ET.SubElement(root, "arguments")
        for arg in self.arguments:
            arg_element = ET.SubElement(args_element, "argument")
            arg_element.text = arg

        return ET.tostring(root, encoding="unicode")


# Example usage:
if __name__ == "__main__":
    scheme = Scheme("Example Scheme")
    scheme.add_argument("arg1")
    scheme.add_argument("arg2")
    print(scheme.to_xml())
