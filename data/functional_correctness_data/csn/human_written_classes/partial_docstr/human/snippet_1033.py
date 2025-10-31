import pandas as pd
from workbench.core.views.pandas_to_view import PandasToView
from workbench.algorithms.dataframe.residuals_calculator import ResidualsCalculator
from workbench.algorithms.dataframe.row_tagger import RowTagger
from workbench.core.views.view import View
from typing import Union
from workbench.api import FeatureSet, Model, Endpoint

class MDQView:
    """MDQView Class: A View that computes various model/feature quality metrics

    Common Usage:
        ```python
        # Grab a FeatureSet and an Endpoint
        fs = FeatureSet("abalone_features")
        endpoint = Endpoint("abalone-regression")

        # Create a ModelDataQuality View
        mdq_view = MDQView.create(fs, endpoint=endpoint, id_column="id")
        my_df = mdq_view.pull_dataframe(limit=5)

        # Query the view
        df = mdq_view.query(f"SELECT * FROM {mdq_view.table} where residuals > 0.5")
        ```
    """

    @classmethod
    def create(cls, fs: FeatureSet, endpoint: Endpoint, id_column: str, use_reference_model: bool=False) -> Union[View, None]:
        """Create a Model Data Quality View with metrics

        Args:
            fs (FeatureSet): The FeatureSet object
            endpoint (Endpoint): The Endpoint object to use for the target and features
            id_column (str): The name of the id column (must be defined for join logic)
            use_reference_model (bool): Use the reference model for inference (default: False)

        Returns:
            Union[View, None]: The created View object (or None if failed)
        """
        fs.log.important('Creating Model Data Quality View...')
        model_input = Model(endpoint.get_input())
        target = model_input.target()
        features = model_input.features()
        df = fs.data_source.query(f'SELECT * FROM {fs.data_source.name}')
        missing_columns = [col for col in [target] + features if col not in df.columns]
        if missing_columns:
            fs.log.error(f'Missing columns in data source: {missing_columns}')
            return None
        categorical_target = not pd.api.types.is_numeric_dtype(df[target])
        row_tagger = RowTagger(df, features=features, id_column=id_column, target_column=target, within_dist=0.25, min_target_diff=1.0, outlier_df=fs.data_source.outliers(), categorical_target=categorical_target)
        mdq_df = row_tagger.tag_rows()
        mdq_df.rename(columns={'tags': 'data_quality_tags'}, inplace=True)
        mdq_df['data_quality'] = mdq_df['data_quality_tags'].apply(cls.calculate_data_quality)
        if use_reference_model:
            residuals_calculator = ResidualsCalculator()
        else:
            residuals_calculator = ResidualsCalculator(endpoint=endpoint)
        residuals_df = residuals_calculator.fit_transform(df[features], df[target])
        residuals_df[id_column] = df[id_column]
        overlap_columns = [col for col in residuals_df.columns if col in mdq_df.columns and col != id_column]
        mdq_df = mdq_df.drop(columns=overlap_columns)
        mdq_df = mdq_df.merge(residuals_df, on=id_column, how='left')
        view_name = 'mdq_ref' if use_reference_model else 'mdq'
        return PandasToView.create(view_name, fs, df=mdq_df, id_column=id_column)

    @staticmethod
    def calculate_data_quality(tags):
        score = 1.0
        if 'coincident' in tags:
            score -= 1.0
        if 'htg' in tags:
            score -= 0.5
        if 'outlier' in tags:
            score -= 0.25
        score = max(0.0, score)
        return score