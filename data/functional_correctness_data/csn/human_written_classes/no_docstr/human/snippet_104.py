class XmlToken:

    def __init__(self, type, name_or_data, attrs=None, line=None, column=None):
        assert type in (XML_ELEMENT_START, XML_ELEMENT_END, XML_CHARACTER_DATA, XML_EOF)
        self.type = type
        self.name_or_data = name_or_data
        self.attrs = attrs
        self.line = line
        self.column = column

    def __str__(self):
        if self.type == XML_ELEMENT_START:
            return '<' + self.name_or_data + ' ...>'
        if self.type == XML_ELEMENT_END:
            return '</' + self.name_or_data + '>'
        if self.type == XML_CHARACTER_DATA:
            return self.name_or_data
        if self.type == XML_EOF:
            return 'end of file'
        assert 0