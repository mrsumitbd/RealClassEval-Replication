from dataclasses import dataclass
import pandas as pd
from utilsforecast.evaluation import evaluate
from functools import partial

@dataclass
class ExperimentDataset:
    df: pd.DataFrame
    freq: str
    h: int
    seasonality: int

    def evaluate_forecast_df(self, forecast_df: pd.DataFrame, models: list[str]) -> pd.DataFrame:
        """
        Parameters
        ----------
        forecast_df : pd.DataFrame
            df should have columns: unique_id, ds, cutoff, y, and models
        """
        for model in models:
            if forecast_df[model].isna().sum() > 0:
                print(forecast_df.loc[forecast_df[model].isna()]['unique_id'].unique())
                raise ValueError(f'model {model} has NaN values')
        cutoffs = forecast_df[['unique_id', 'cutoff']].drop_duplicates()
        train_cv_splits = generate_train_cv_splits(df=self.df, cutoffs=cutoffs)

        def add_id_cutoff(df: pd.DataFrame):
            df['id_cutoff'] = df['unique_id'].astype(str) + '-' + df['cutoff'].astype(str)
        for df in [cutoffs, train_cv_splits, forecast_df]:
            add_id_cutoff(df)
        partial_mase = partial(mase, seasonality=self.seasonality)
        eval_df = evaluate(df=forecast_df, train_df=train_cv_splits, metrics=[partial_mase], models=models, id_col='id_cutoff')
        eval_df = eval_df.merge(cutoffs, on=['id_cutoff'])
        eval_df = eval_df.drop(columns=['id_cutoff'])
        eval_df = eval_df[['unique_id', 'cutoff', 'metric'] + models]
        return eval_df