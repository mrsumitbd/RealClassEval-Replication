class Scheme:

    def __init__(self, title):
        if title is None:
            raise ValueError("title cannot be None")
        self.title = str(title)
        self._arguments = []

    def add_argument(self, arg):
        if arg is None:
            raise ValueError("arg cannot be None")
        self._arguments.append(arg)

    def to_xml(self):
        def _escape(text):
            s = str(text)
            s = s.replace("&", "&amp;")
            s = s.replace("<", "&lt;")
            s = s.replace(">", "&gt;")
            s = s.replace('"', "&quot;")
            s = s.replace("'", "&apos;")
            return s

        lines = []
        lines.append(f'<scheme title="{_escape(self.title)}">')
        for arg in self._arguments:
            if hasattr(arg, "to_xml") and callable(getattr(arg, "to_xml")):
                xml = arg.to_xml()
                lines.append(xml if xml is not None else "<argument/>")
            else:
                lines.append(f"  <argument>{_escape(arg)}</argument>")
        lines.append("</scheme>")
        return "\n".join(lines)
