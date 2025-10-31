from pathlib import Path
import pandas as pd
from dataclasses import dataclass

@dataclass
class ForecastDataset:
    forecast_df: pd.DataFrame
    time_df: pd.DataFrame

    @classmethod
    def from_dir(cls, dir: str | Path):
        dir_ = Path(dir)
        forecast_df = pd.read_parquet(dir_ / 'forecast_df.parquet')
        time_df = pd.read_parquet(dir_ / 'time_df.parquet')
        return cls(forecast_df=forecast_df, time_df=time_df)

    @staticmethod
    def is_forecast_ready(dir: str | Path):
        dir_ = Path(dir)
        forecast_path = dir_ / 'forecast_df.parquet'
        time_path = dir_ / 'time_df.parquet'
        return forecast_path.exists() and time_path.exists()

    def save_to_dir(self, dir: str | Path):
        dir_ = Path(dir)
        dir_.mkdir(parents=True, exist_ok=True)
        self.forecast_df.to_parquet(dir_ / 'forecast_df.parquet')
        self.time_df.to_parquet(dir_ / 'time_df.parquet')