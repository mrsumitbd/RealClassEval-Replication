class PublishDatePattern:
    """Ensure correctly formed publish date patterns; to be used in conjuntion with the configuration
    `known_publish_date_tags` property

    Args:
        attr (str): The attribute type: class, id, etc
        value (str): The value of the attribute
        content (str): The name of another attribute (of the element) that contains the value
        subcontent (str): The name of a json object key (optional)
        tag (str): The type of tag, such as `time` that contains the publish date
        domain (str): The domain to which this pattern pertains (optional)
    Note:
        Must provide, at a minimum, (attr and value) or (tag)
    """
    __slots__ = ['attr', 'value', 'content', 'subcontent', 'tag', 'domain']

    def __init__(self, *, attr=None, value=None, content=None, subcontent=None, tag=None, domain=None):
        if (not attr and (not value)) and (not tag):
            raise Exception('`attr` and `value` must be set or `tag` must be set')
        self.attr = attr
        self.value = value
        self.content = content
        self.subcontent = subcontent
        self.tag = tag
        self.domain = domain

    def __repr__(self):
        if self.tag:
            return f'PublishDatePattern(tag={self.tag}, attr={self.attr}, value={self.value} domain={self.domain})'
        res = f'PublishDatePattern(attr={self.attr}, value={self.value} content={self.content} subcontent={self.subcontent} domain={self.domain})'
        return res