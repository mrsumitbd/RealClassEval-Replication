from string import Template
import os

class DiasporaHCard:
    """Diaspora hCard document.

    Must receive the `required` attributes as keyword arguments to init.
    """
    required = ['hostname', 'fullname', 'firstname', 'lastname', 'photo300', 'photo100', 'photo50', 'searchable', 'guid', 'public_key', 'username']

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'hcard_diaspora.html')
        with open(template_path) as f:
            self.template = Template(f.read())

    def render(self):
        required = self.required[:]
        for key, value in self.kwargs.items():
            required.remove(key)
            assert value is not None
            assert isinstance(value, str)
        assert len(required) == 0
        return self.template.substitute(self.kwargs)