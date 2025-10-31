from inscriptis.model.html_element import DEFAULT_HTML_ELEMENT, HtmlElement
from copy import copy
from collections import defaultdict

class AnnotationModel:
    """Adapt the CSS profile and CSS attributes for annotation support.

    Attributes:
        css: the refined CSS class which contains annotations for HtmlElements
             which should be annotated.
        css_attr: information on CSS attributes that shall be annotated.
    """

    def __init__(self, css_profile, model: dict):
        tags, self.css_attr = self._parse(model)
        for tag, annotations in tags.items():
            if tag not in css_profile:
                css_profile[tag] = copy(DEFAULT_HTML_ELEMENT)
            css_profile[tag].annotation += tuple(annotations)
        self.css = css_profile

    @staticmethod
    def _parse(model: dict) -> tuple[dict, list]:
        """Compute the AnnotationModel from a model dictionary.

        Returns:
            the AnnotationModel matching the input dictionary.
        """
        tags = defaultdict(list)
        attrs = []
        for key, annotations in model.items():
            if '#' in key:
                tag, attr = key.split('#')
                if '=' in attr:
                    attr, value = attr.split('=')
                else:
                    value = None
                attrs.append(ApplyAnnotation(annotations, attr, tag, value))
            else:
                tags[key].extend(annotations)
        return (tags, attrs)