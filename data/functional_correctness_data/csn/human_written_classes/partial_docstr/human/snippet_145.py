from lazy_op import LazyOpResult, to_weld_type
import utils
import grizzly_impl
from seriesweld import SeriesWeld

class GroupByWeldSeries:
    """Summary

    Attributes:
        column_name
        column_type
        column,
        grouping_column
    """

    def __init__(self, name, column, column_type, grouping_column_names, grouping_columns, grouping_column_types):
        self.name = name
        self.column = column
        self.column_type = column_type
        self.grouping_column_names = grouping_column_names
        self.grouping_columns = grouping_columns
        self.grouping_column_types = grouping_column_types

    def std(self):
        """Standard deviation

        Note that is by default normalizd by n - 1
        # TODO, what does pandas do for multiple grouping columns?
        # Currently we are just going to use one grouping column
        """
        std_expr = grizzly_impl.groupby_std([self.column], [self.column_type], self.grouping_columns, self.grouping_column_types)
        unzipped_columns = grizzly_impl.unzip_columns(std_expr, self.grouping_column_types + [WeldDouble()])
        index_expr = LazyOpResult(grizzly_impl.get_field(unzipped_columns, 0), self.grouping_column_types[0], 1)
        column_expr = LazyOpResult(grizzly_impl.get_field(unzipped_columns, 1), self.grouping_column_types[0], 1)
        group_expr = utils.group([index_expr, column_expr])
        return SeriesWeld(group_expr.expr, WeldDouble(), index_type=self.grouping_column_types[0], index_name=self.grouping_column_names[0])