
import os
import sys
from string import Template as StrTemplate


class Template:
    def __init__(self):
        pass

    def render(self, sources, config, out=sys.stdout):
        """
        Render a template from the given sources using the provided config dictionary.
        `sources` can be a single string (template text or file path) or an iterable of such.
        The rendered output is written to the file-like object `out`.
        """
        # Gather template text
        if isinstance(sources, (str, bytes)):
            sources = [sources]
        template_parts = []
        for src in sources:
            if isinstance(src, (bytes, bytearray)):
                template_parts.append(src.decode('utf-8'))
            elif isinstance(src, str):
                if os.path.isfile(src):
                    with open(src, 'r', encoding='utf-8') as f:
                        template_parts.append(f.read())
                else:
                    template_parts.append(src)
            else:
                raise TypeError(f"Unsupported source type: {type(src)}")
        template_text = ''.join(template_parts)

        # Create a string.Template and substitute
        tmpl = StrTemplate(template_text)
        rendered = tmpl.safe_substitute(config)

        # Write to output
        out.write(rendered)
        if hasattr(out, 'flush'):
            out.flush()
