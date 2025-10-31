class LEMSXMLNode:

    def __init__(self, pyxmlnode):
        self.tag = get_nons_tag_from_node(pyxmlnode)
        self.ltag = self.tag.lower()
        self.attrib = dict()
        self.lattrib = dict()
        for k in pyxmlnode.attrib:
            self.attrib[k] = pyxmlnode.attrib[k]
            self.lattrib[k.lower()] = pyxmlnode.attrib[k]
        self.children = list()
        for pyxmlchild in pyxmlnode:
            self.children.append(LEMSXMLNode(pyxmlchild))

    def __str__(self):
        return 'LEMSXMLNode <{0} {1}>'.format(self.tag, self.attrib)