class ArticleContextPattern:
    """Help ensure correctly generated article context patterns

    Args:
        attr (str): The attribute type: class, id, etc
        value (str): The value of the attribute
        tag (str): The type of tag, such as `article` that contains the main article body
        domain (str): The domain to which this pattern pertains (optional)
    Note:
        Must provide, at a minimum, (attr and value) or (tag)
    """
    __slots__ = ['attr', 'value', 'tag', 'domain']

    def __init__(self, *, attr=None, value=None, tag=None, domain=None):
        if (not attr and (not value)) and (not tag):
            raise Exception('`attr` and `value` must be set or `tag` must be set')
        self.attr = attr
        self.value = value
        self.tag = tag
        self.domain = domain

    def __repr__(self):
        return f'ArticleContextPattern(attr={self.attr} value={self.value} tag={self.tag} domain={self.domain})'