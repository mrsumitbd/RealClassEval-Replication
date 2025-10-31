import os

class Eio:
    """
    Class describing a .eio file.

    Parameters
    ----------
    path: str
        Path of the .eio file
    """

    def __init__(self, path):
        if not os.path.isfile(path):
            raise FileNotFoundError("No file at given path: '%s'." % path)
        self._path = path
        self._tables_d = parse_eio(self._path)

    def get_table_refs(self):
        """
        Get eio table references.

        Returns
        -------
        typing.Iterator[str]
            Eio table references
        """
        return self._tables_d.keys()

    def get_df(self, table_ref):
        """
        Get the content of a table of the .eio file as a dataframe.

        Parameters
        ----------
        table_ref: str
            table reference

        Returns
        -------
        pandas.DataFrame
        """
        return self._tables_d[table_ref.lower()].get_df()

    def get_value(self, table_ref, column_name_or_i, filter_column_name_or_i, filter_criterion):
        """
        Get first occurrence of value of filter column matching filter criterion.

        Parameters
        ----------
        table_ref: str
        column_name_or_i: str or int
        filter_column_name_or_i: str or int
        filter_criterion: str
        """
        lower_ref = table_ref.lower()
        if lower_ref not in self._tables_d:
            raise KeyError("Unknown table_ref: '%s'." % table_ref)
        return self._tables_d[lower_ref].get_value(column_name_or_i, filter_column_name_or_i, filter_criterion)