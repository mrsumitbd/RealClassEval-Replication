from workbench.utils import pandas_utils
from workbench.core.transforms.pandas_transforms.data_to_pandas import DataToPandas
import logging

class DataSourceEDA:

    def __init__(self, data_source_name: str):
        """DataSourceEDA: Provide basic EDA (Exploratory Data Analysis) for a DataSource
        Args:
            data_source_name (AthenaSource): DataSource for Exploratory Data Analysis"""
        self.log = logging.getLogger('workbench')
        self.data_source_name = data_source_name
        self.data_to_pandas = DataToPandas(self.data_source_name)
        self.log.info(f'Getting DataFrame from {self.data_source_name}...')
        self.data_to_pandas.transform()
        self.df = self.data_to_pandas.get_output()

    def get_column_info(self):
        """Return the Column Information for the DataSource"""
        column_info_df = pandas_utils.info(self.df)
        return column_info_df

    def get_numeric_stats(self):
        """Return the Column Information for the DataSource"""
        stats_df = pandas_utils.numeric_stats(self.df)
        return stats_df