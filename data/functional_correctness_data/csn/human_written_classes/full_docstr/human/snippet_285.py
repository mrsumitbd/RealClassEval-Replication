class RIOTag:
    """Rasterio wrapper to allow da.store on tag."""

    def __init__(self, rfile, name):
        """Init the rasterio tag."""
        self.rfile = rfile
        self.name = name

    def __setitem__(self, key, item):
        """Put the data in the tag."""
        kwargs = {self.name: item.item()}
        self.rfile.update_tags(**kwargs)

    def close(self):
        """Close the file."""
        return self.rfile.close()