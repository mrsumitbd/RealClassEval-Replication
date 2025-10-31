import os
from kibitzr.stash import LazyStash

class JinjaTransform:

    def __init__(self, code, conf):
        from jinja2 import Environment
        environment = Environment()
        environment.filters['text'] = text_filter
        environment.filters['int'] = int_filter
        environment.filters['float'] = float_filter
        environment.filters['dollars'] = dollars_filter
        self.template = environment.from_string(code)
        self.conf = conf

    def render(self, content, context=None):
        from jinja2 import TemplateError
        try:
            return (True, self.template.render(context or self.context(content)))
        except TemplateError:
            logger.warning('Jinja render failed', exc_info=True)
            return (False, None)
    __call__ = render

    def context(self, content):
        html = LazyHTML(content)
        xml = LazyXML(content)
        return {'conf': self.conf, 'stash': LazyStash(), 'content': content, 'lines': content.splitlines(), 'json': LazyJSON(content), 'css': html.css, 'xpath': xml.xpath, 'env': os.environ}