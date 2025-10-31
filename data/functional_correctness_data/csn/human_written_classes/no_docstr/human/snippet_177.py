class ElementTree:

    def __init__(self, root):
        self.root = root

    def write(self, filename, xml_declaration=True):
        with open(filename, 'w') as f:
            if xml_declaration:
                f.write('<?xml version="1.0"?>\n')
            self.root.write(f)