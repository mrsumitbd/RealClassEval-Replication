from django.utils.encoding import force_str, iri_to_uri
from el_pagination import loaders, settings, utils
from django.template import loader

class ELPage:
    """A page link representation.

    Interesting attributes:

        - *self.number*: the page number;
        - *self.label*: the label of the link
          (usually the page number as string);
        - *self.url*: the url of the page (strting with "?");
        - *self.path*: the path of the page;

        - *self.is_current*: return True if page is the current page displayed;
        - *self.is_first*: return True if page is the first page;
        - *self.is_last*:  return True if page is the last page.
    """

    def __init__(self, request, number, current_number, total_number, querystring_key, label=None, default_number=1, override_path=None, context=None):
        self._request = request
        self.number = number
        self.label = force_str(number) if label is None else label
        self.querystring_key = querystring_key
        self.context = context or {}
        self.context['request'] = request
        self.is_current = number == current_number
        self.is_first = number == 1
        self.is_last = number == total_number
        if settings.USE_NEXT_PREVIOUS_LINKS:
            self.is_previous = label and number == current_number - 1
            self.is_next = label and number == current_number + 1
        self.url = utils.get_querystring_for_page(request, number, self.querystring_key, default_number=default_number)
        path = iri_to_uri(override_path or request.path)
        self.path = f'{path}{self.url}'

    def render_link(self):
        """Render the page as a link."""
        extra_context = {'add_nofollow': settings.ADD_NOFOLLOW, 'page': self, 'querystring_key': self.querystring_key}
        if self.is_current:
            template_name = 'el_pagination/current_link.html'
        else:
            template_name = 'el_pagination/page_link.html'
            if settings.USE_NEXT_PREVIOUS_LINKS:
                if self.is_previous:
                    template_name = 'el_pagination/previous_link.html'
                if self.is_next:
                    template_name = 'el_pagination/next_link.html'
        if template_name not in _template_cache:
            _template_cache[template_name] = loader.get_template(template_name)
        template = _template_cache[template_name]
        with self.context.push(**extra_context):
            return template.render(self.context.flatten())