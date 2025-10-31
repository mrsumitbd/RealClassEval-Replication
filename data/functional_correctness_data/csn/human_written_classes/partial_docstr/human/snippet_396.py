class AuthorPattern:
    """Ensures that the author patterns are correctly formed for use with the `known_author_patterns` of configuration

    Args:
        attr (str): The attribute type: class, id, etc
        value (str): The value of the attribute
        content (str): The name of another attribute (of the element) that contains the value
        tag (str): The type of tag, such as `author` that contains the author information
        subpattern (str): A subpattern for elements within the main attribute
    """
    __slots__ = ['attr', 'value', 'content', 'tag', 'subpattern']

    def __init__(self, *, attr=None, value=None, content=None, tag=None, subpattern=None):
        if (not attr and (not value)) and (not tag):
            raise Exception('`attr` and `value` must be set or `tag` must be set')
        self.attr = attr
        self.value = value
        self.content = content
        self.tag = tag
        self.subpattern = subpattern

    def __repr__(self):
        if self.tag:
            return f'AuthorPattern(tag={self.tag}, attr={self.attr}, value={self.value})'
        res = f'AuthorPattern(attr={self.attr}, value={self.value} content={self.content} subpattern={self.subpattern})'
        return res