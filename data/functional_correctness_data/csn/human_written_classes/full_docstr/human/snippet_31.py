import grizzly_impl

class StringSeriesWeld:
    """Summary

    Attributes:
        column_name (TYPE): Description
        df (TYPE): Description
        dim (int): Description
        expr (TYPE): Description
        weld_type (TYPE): Description
    """

    def __init__(self, expr, weld_type, df=None, column_name=None):
        """Summary

        Args:
            expr (TYPE): Description
            weld_type (TYPE): Description
            df (None, optional): Description
            column_name (None, optional): Description
        """
        self.expr = expr
        self.weld_type = weld_type
        self.dim = 1
        self.df = df
        self.column_name = column_name

    def slice(self, start, size):
        """Summary

        Args:
            start (TYPE): Description
            size (TYPE): Description

        Returns:
            TYPE: Description
        """
        return SeriesWeld(grizzly_impl.slice(self.expr, start, size, self.weld_type), self.weld_type, self.df, self.column_name)