import re
from docutils import nodes

class ANSIHTMLParser:

    def __call__(self, app, doctree, docname):
        handler = self._format_it
        if app.builder.name not in ['html', 'readthedocs']:
            handler = self._strip_color_from_block_content
        for ansi_block in doctree.traverse(python_terminal_block):
            handler(ansi_block)

    def _strip_color_from_block_content(self, block):
        content = re.sub('\x1b\\[([^m]+)m', '', block.rawsource)
        literal_node = nodes.literal_block(content, content)
        block.replace_self(literal_node)

    def _format_it(self, block):
        source = block.rawsource
        content = htmlize(source)
        formatted = '<pre>{}</pre>'.format(content)
        raw_node = nodes.raw(formatted, formatted, format='html')
        block.replace_self(raw_node)