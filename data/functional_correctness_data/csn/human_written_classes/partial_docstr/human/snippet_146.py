import grizzly_impl

class WeldLocIndexer:
    """
    Label location based indexer for selection by label for Series objects.

    Attributes:
        grizzly_obj (TYPE): The Series being indexed into.
    """

    def __init__(self, grizzly_obj):
        self.grizzly_obj = grizzly_obj

    def __getitem__(self, key):
        if isinstance(self.grizzly_obj, SeriesWeld):
            series = self.grizzly_obj
            if isinstance(key, SeriesWeld):
                if series.index_type is not None:
                    index_expr = grizzly_impl.get_field(series.expr, 0)
                    column_expr = grizzly_impl.get_field(series.expr, 1)
                    zip_expr = grizzly_impl.zip_columns([index_expr, column_expr])
                    predicate_expr = grizzly_impl.isin(index_expr, key.expr, series.index_type)
                    filtered_expr = grizzly_impl.filter(zip_expr, predicate_expr)
                    unzip_expr = grizzly_impl.unzip_columns(filtered_expr, [series.index_type, series.weld_type])
                    return SeriesWeld(unzip_expr, series.weld_type, series.df, series.column_name, series.index_type, series.index_name)
        raise Exception('Cannot invoke getitem on non SeriesWeld object')