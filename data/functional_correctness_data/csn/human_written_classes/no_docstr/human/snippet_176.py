class Element:

    def __init__(self, name, **kwargs):
        self.name = name
        self.attrib = kwargs
        self._children = []
        self.text = None
        self.text_writer = None

    def insert(self, pos, elem):
        self._children.insert(pos, elem)

    def set(self, key, value):
        self.attrib[key] = value

    def write(self, f):
        kw_list = [f'{key}="{value}"' for key, value in self.attrib.items()]
        f.write('<{}>\n'.format(' '.join([self.name] + kw_list)))
        if self.text:
            f.write(self.text)
            f.write('\n')
        if self.text_writer:
            self.text_writer(f)
            f.write('\n')
        for child in self._children:
            child.write(f)
        f.write(f'</{self.name}>\n')