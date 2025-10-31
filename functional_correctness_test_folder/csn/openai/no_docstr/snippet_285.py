
class RIOTag:
    def __init__(self, rfile, name):
        """
        Create a new RIOTag instance.

        Parameters
        ----------
        rfile : file-like object
            The file to which the tag will be written.
        name : str
            The name of the tag.
        """
        self.rfile = rfile
        self.name = name
        self._attrs = {}

    def __setitem__(self, key, item):
        """
        Set an attribute for the tag.

        Parameters
        ----------
        key : str
            The attribute name.
        item : Any
            The attribute value.
        """
        self._attrs[key] = item

    def close(self):
        """
        Write the tag to the file and close the tag.

        The tag is written as a self‑closing tag, e.g.
        <tag key="value" />.
        """
        attrs = ' '.join(f'{k}="{v}"' for k, v in self._attrs.items())
        if attrs:
            self.rfile.write(f'<{self.name} {attrs} />\n')
        else:
            self.rfile.write(f'<{self.name} />\n')
