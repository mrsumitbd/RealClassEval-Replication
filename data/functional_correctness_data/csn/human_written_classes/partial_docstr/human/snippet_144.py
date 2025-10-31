from seriesweld import SeriesWeld
import grizzly_impl

class DataFrameWeldLoc:
    """
    Label location based indexer for selection by label for dataframe objects.

    Attributes:
        df (TYPE): The DataFrame  being indexed into.
    """

    def __init__(self, df):
        self.df = df

    def __getitem__(self, key):
        if isinstance(key, SeriesWeld):
            index_expr = grizzly_impl.get_field(self.df.expr, 0)
            if self.df.is_pivot:
                index_type, pivot_type, column_type = self.df.column_types
                index_elem_type = index_type.elemType
                index_expr_predicate = grizzly_impl.isin(index_expr, key.expr, index_elem_type)
                return DataFrameWeldExpr(grizzly_impl.pivot_filter(self.df.expr, index_expr_predicate), self.df.column_names, self.df.weld_type, is_pivot=True)
        raise Exception('Cannot invoke getitem on an object that is not SeriesWeld')