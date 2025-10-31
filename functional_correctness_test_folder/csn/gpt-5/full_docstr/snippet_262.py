import warnings
from typing import List, Tuple, Optional, Union

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    import seaborn as sns
    _HAS_SNS = True
except Exception:
    _HAS_SNS = False


class Plot_Data:
    ''' This class contains functions for displaying various plots.
    Attributes
    ----------
    count    : int
        Keeps track of the number of figures.
    '''

    def __init__(self, figsize: Tuple[float, float] = (18, 5)):
        ''' Constructor.
        Parameters
        ----------
        figsize : tuple
            Size of figure.
        '''
        self.figsize = figsize
        self.count = 0

    def correlation_plot(self, data: pd.DataFrame):
        ''' Create heatmap of Pearson's correlation coefficient.
        Parameters
        ----------
        data    : pd.DataFrame()
            Data to display.
        Returns
        -------
        matplotlib.figure
            Heatmap.
        '''
        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame.")
        if data.empty:
            raise ValueError("data must not be empty.")

        corr = data.corr(method='pearson', numeric_only=True)

        self.count += 1
        fig, ax = plt.subplots(figsize=self.figsize)
        if _HAS_SNS:
            sns = __import__("seaborn")
            heat = sns.heatmap(
                corr,
                ax=ax,
                annot=True,
                fmt=".2f",
                cmap="coolwarm",
                square=True,
                cbar_kws={"shrink": 0.8},
                linewidths=0.5,
                linecolor='white'
            )
            heat.set_title("Pearson Correlation Heatmap")
        else:
            cax = ax.imshow(corr.values, cmap="coolwarm", vmin=-1, vmax=1)
            fig.colorbar(cax, ax=ax, shrink=0.8)
            ax.set_xticks(range(len(corr.columns)))
            ax.set_yticks(range(len(corr.index)))
            ax.set_xticklabels(corr.columns, rotation=45, ha="right")
            ax.set_yticklabels(corr.index)
            ax.set_title("Pearson Correlation Heatmap")
            # Add annotations
            for (i, j), val in np.ndenumerate(corr.values):
                ax.text(j, i, f"{val:.2f}", ha="center",
                        va="center", color="black")

        fig.tight_layout()
        return fig

    def baseline_projection_plot(
        self,
        y_true: pd.Series,
        y_pred: np.ndarray,
        baseline_period: List[str],
        projection_period: List[str],
        model_name: str,
        adj_r2: float,
        data: pd.DataFrame,
        input_col: List[str],
        output_col: str,
        model,
        site: Optional[str] = None
    ):
        ''' Create baseline and projection plots.
        Parameters
        ----------
        y_true              : pd.Series()
            Actual y values.
        y_pred              : np.ndarray
            Predicted y values.
        baseline_period     : list(str)
            Baseline period.
        projection_period   : list(str)
            Projection periods.
        model_name          : str
            Optimal model's name.
        adj_r2              : float
            Adjusted R2 score of optimal model.
        data                : pd.Dataframe()
            Data containing real values.
        input_col           : list(str)
            Predictor column(s).
        output_col          : str
            Target column.
        model               : func
            Optimal model.
        Returns
        -------
        matplotlib.figure
            Baseline plot
        '''
        if not isinstance(y_true, pd.Series):
            raise TypeError("y_true must be a pandas Series.")
        if not isinstance(y_pred, (np.ndarray, list, pd.Series)):
            raise TypeError("y_pred must be an array-like of predictions.")
        y_pred = np.asarray(y_pred)

        if y_true.empty:
            raise ValueError("y_true must not be empty.")
        if y_true.index is None or not isinstance(y_true.index, pd.Index):
            raise ValueError(
                "y_true must have an index (ideally DatetimeIndex).")

        if len(baseline_period) != 2 or len(projection_period) != 2:
            raise ValueError(
                "baseline_period and projection_period must be [start, end].")

        # Convert periods to timestamps if possible
        def _to_ts(v):
            try:
                return pd.to_datetime(v)
            except Exception:
                return v

        b_start, b_end = map(_to_ts, baseline_period)
        p_start, p_end = map(_to_ts, projection_period)

        # Align baseline true/pred
        if len(y_pred) != len(y_true):
            warnings.warn(
                "Length of y_pred does not match y_true. Aligning to min length.")
        n = min(len(y_true), len(y_pred))
        y_true_baseline = y_true.iloc[:n]
        y_pred_baseline = pd.Series(
            y_pred[:n], index=y_true_baseline.index, name="Prediction")

        # Restrict to baseline window if index is slicable
        try:
            y_true_baseline = y_true_baseline.loc[b_start:b_end]
            y_pred_baseline = y_pred_baseline.loc[b_start:b_end]
        except Exception:
            pass

        # Prepare projection data
        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame.")
        for col in input_col + [output_col]:
            if col not in data.columns:
                raise ValueError(f"Column '{col}' not found in data.")

        try:
            data_proj = data.loc[p_start:p_end]
        except Exception:
            # if index is not datetime-like, try boolean mask using a 'date' column if present
            if 'date' in data.columns:
                dates = pd.to_datetime(data['date'], errors='coerce')
                mask = (dates >= pd.to_datetime(p_start)) & (
                    dates <= pd.to_datetime(p_end))
                data_proj = data.loc[mask]
            else:
                data_proj = data.copy()

        X_proj = data_proj[input_col]
        y_proj_true = data_proj[output_col]

        # Predict using provided model
        try:
            if hasattr(model, "predict"):
                y_proj_pred_vals = model.predict(X_proj)
            else:
                y_proj_pred_vals = model(X_proj)
        except Exception as e:
            warnings.warn(
                f"Projection prediction failed with error: {e}. Using NaNs.")
            y_proj_pred_vals = np.full(len(X_proj), np.nan)

        y_proj_pred = pd.Series(np.asarray(
            y_proj_pred_vals).ravel(), index=X_proj.index, name="Prediction")

        # Plot
        self.count += 1
        fig, axes = plt.subplots(1, 2, figsize=self.figsize, sharey=False)

        ax0 = axes[0]
        ax0.plot(y_true_baseline.index, y_true_baseline.values,
                 label="Actual", color="#1f77b4", linewidth=2)
        ax0.plot(y_pred_baseline.index, y_pred_baseline.values,
                 label="Predicted", color="#ff7f0e", linewidth=2, alpha=0.9)
        ax0.set_title("Baseline")
        ax0.set_xlabel("Time")
        ax0.set_ylabel(output_col if isinstance(output_col, str) else "Value")
        ax0.legend()
        ax0.grid(True, alpha=0.3)

        ax1 = axes[1]
        ax1.plot(y_proj_true.index, y_proj_true.values,
                 label="Actual", color="#1f77b4", linewidth=2)
        ax1.plot(y_proj_pred.index, y_proj_pred.values,
                 label="Predicted", color="#ff7f0e", linewidth=2, alpha=0.9)
        ax1.set_title("Projection")
        ax1.set_xlabel("Time")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        site_str = f" | Site: {site}" if site else ""
        fig.suptitle(
            f"{model_name}{site_str} | Adj. R2 = {adj_r2:.3f}", fontsize=14)
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])

        return fig
