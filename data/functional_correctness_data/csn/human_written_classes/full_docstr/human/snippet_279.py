class SearchDumperExt:
    """Interface for Search dumper extensions."""

    def dump(self, record, data):
        """Dump the data."""

    def load(self, data, record_cls):
        """Load the data.

        Reverse the changes made by the dump method.
        """