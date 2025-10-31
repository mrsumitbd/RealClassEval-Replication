from inscriptis.model.html_element import DEFAULT_HTML_ELEMENT, HtmlElement

class ApplyAnnotation:
    """Apply an Annotation to the given attribute.

    Arguments:
        annotations: a tuple of annotations to be applied to the attribute.
        attr: the name of the attribute.
        match_tag: only apply annotations to attributes that belong to the
                   given match_tag.
        match_value: only apply annotations to attribute with the given
                     match_value.
    """
    __slots__ = ('annotations', 'attr', 'match_tag', 'match_value', 'matcher')

    def __init__(self, annotations: tuple, attr: str, match_tag: str='', match_value: str=''):
        self.annotations = tuple(annotations)
        self.attr = attr
        self.match_tag = match_tag
        self.match_value = match_value

    def apply(self, attr_value: str, html_element: HtmlElement):
        """Apply the annotation to HtmlElements with matching tags."""
        if self.match_tag and self.match_tag != html_element.tag or (self.match_value and self.match_value not in attr_value.split()):
            return
        html_element.annotation += self.annotations

    def __str__(self):
        return '<ApplyAnnotation: {tag}#{attr}={value}'.format(tag=self.match_tag or '{any}', attr=self.attr or '{any}', value=self.match_value or '{any}')
    __repr__ = __str__