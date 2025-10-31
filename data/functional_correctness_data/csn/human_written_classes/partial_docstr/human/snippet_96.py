from django.template import Template
from crispy_forms.utils import TEMPLATE_PACK, flatatt, render_field

class HTML:
    """
    Layout object. It can contain pure HTML and it has access to the whole
    context of the page where the form is being rendered.

    Examples::

        HTML("{% if saved %}Data saved{% endif %}")
        HTML('<input type="hidden" name="{{ step_field }}" value="{{ step0 }}" />')
    """

    def __init__(self, html):
        self.html = html

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        return Template(str(self.html)).render(context)