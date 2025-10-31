class ContentCollector:
    """
    Collect content during view processing, and substitute in response by finding magic strings.

    This enables view functionality, such as template tags, to introduce content such as css and js
    inclusion into the header and footer.
    """

    def __init__(self):
        self.header_placeholder = 'DJANGO_PLOTLY_DASH_HEADER_PLACEHOLDER'
        self.footer_placeholder = 'DJANGO_PLOTLY_DASH_FOOTER_PLACEHOLDER'
        self.embedded_holder = EmbeddedHolder()
        self._encoding = 'utf-8'

    def adjust_response(self, response):
        """Locate placeholder magic strings and replace with content"""
        try:
            c1 = self._replace(response.content, self.header_placeholder, self.embedded_holder.css)
            response.content = self._replace(c1, self.footer_placeholder, '\n'.join([self.embedded_holder.config, self.embedded_holder.scripts]))
        except AttributeError:
            pass
        return response

    def _replace(self, content, placeholder, substitution):
        return content.replace(self._encode(placeholder), self._encode(substitution if substitution else ''))

    def _encode(self, string):
        return string.encode(self._encoding)