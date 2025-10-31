class TaggedValue:
    """A value tagged in a ``.yml`` file"""

    def __init__(self, value, tag):
        """
        :param value: the tagged value
        :type value: str
        :param tag: the yaml tag, with or without the syntactically required ``!``
        :type tag: str
        """
        self.value = value
        self.tag = tag[1:] if tag.startswith('!') else tag

    def __repr__(self):
        return f'TaggedValue(value={self.value}, tag={self.tag})'