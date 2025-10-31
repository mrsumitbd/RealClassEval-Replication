import pandas as pd

class EioTable:
    """
    Class describing a table of a .eio file.

    Parameters
    ----------
    ref: str
    columns: list of str
    """

    def __init__(self, ref, columns, data):
        col_len = len(columns)
        for i, r in enumerate(data):
            if len(r) != col_len:
                raise RuntimeError('Wrong number of columns in row %i of table %s.' % (i, ref))
        self._ref = ref
        self._columns = columns
        self._data = data

    def _get_column_index(self, column_name_or_i):
        if isinstance(column_name_or_i, int) or isinstance(column_name_or_i, float):
            return column_name_or_i
        if column_name_or_i not in self._columns:
            raise KeyError("Unknown column '%s' for table '%s'." % (column_name_or_i, self._ref))
        return self._columns.index(column_name_or_i)

    def get_df(self):
        """
        Get table data as a data frame.

        Returns
        -------
        pandas.DataFrame
        """
        _df = pd.DataFrame(data=self._data, columns=self._columns, dtype='object')
        _df.name = self._ref
        return _df

    def get_value(self, column_name_or_i, filter_column_name_or_i, filter_criterion):
        """
        Return first occurrence of value of filter column matching filter criterion.

        Parameters
        ----------
        column_name_or_i: str or int
        filter_column_name_or_i: str or int
        filter_criterion: str
        """
        column_i = self._get_column_index(column_name_or_i)
        filter_column_i = self._get_column_index(filter_column_name_or_i)
        filter_fct = {float: lambda x: float(x) == filter_criterion, int: lambda x: int(x) == filter_criterion, str: lambda x: x.lower() == filter_criterion.lower()}[type(filter_criterion)]
        for row_i, row in enumerate(self._data):
            if filter_fct(row[filter_column_i]):
                break
        else:
            raise ValueError('Filter did not return any values.')
        return self._data[row_i][column_i]