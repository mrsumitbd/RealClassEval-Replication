import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Union, Tuple


class Plot_Data:
    ''' This class contains functions for displaying various plots.
    Attributes
    ----------
    count    : int
        Keeps track of the number of figures.
    '''

    def __init__(self, figsize=(18, 5)):
        self.figsize = figsize
        self.count = 0
        sns.set_style("whitegrid")

    def correlation_plot(self, data):
        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame")
        corr = data.select_dtypes(include=[np.number]).corr()
        mask = np.triu(np.ones_like(corr, dtype=bool))
        fig, ax = plt.subplots(figsize=self.figsize)
        sns.heatmap(
            corr,
            mask=mask,
            cmap="coolwarm",
            annot=True,
            fmt=".2f",
            square=True,
            cbar_kws={"shrink": 0.8},
            ax=ax
        )
        ax.set_title("Correlation Heatmap")
        plt.tight_layout()
        self.count += 1
        return fig

    def baseline_projection_plot(self, y_true, y_pred, baseline_period, projection_period, model_name, adj_r2, data, input_col, output_col, model, site):
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
        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame")
        if isinstance(input_col, str):
            input_cols = [input_col]
        else:
            input_cols = list(input_col)

        # Ensure datetime index for slicing
        df = data.copy()
        if not isinstance(df.index, pd.DatetimeIndex):
            try:
                df.index = pd.to_datetime(df.index)
            except Exception as e:
                raise ValueError(
                    "DataFrame index must be datetime-like or convertible to datetime.") from e

        def _build_mask(period_spec) -> pd.Series:
            # Supports ["start", "end"] or list of such pairs
            if isinstance(period_spec, (list, tuple)) and len(period_spec) == 2 and all(isinstance(x, str) for x in period_spec):
                start, end = pd.to_datetime(
                    period_spec[0]), pd.to_datetime(period_spec[1])
                return (df.index >= start) & (df.index <= end)
            # If list of pairs
            mask = pd.Series(False, index=df.index)
            for item in period_spec:
                if isinstance(item, (list, tuple)) and len(item) == 2:
                    start, end = pd.to_datetime(
                        item[0]), pd.to_datetime(item[1])
                    mask |= ((df.index >= start) & (df.index <= end))
            return mask

        # Baseline period mask
        base_mask = _build_mask(baseline_period)

        # Align y_true and y_pred for baseline
        if not isinstance(y_true, (pd.Series, pd.DataFrame)):
            y_true = pd.Series(y_true, index=df.index[base_mask])
        else:
            if not isinstance(y_true.index, pd.DatetimeIndex):
                try:
                    y_true.index = pd.to_datetime(y_true.index)
                except Exception as e:
                    raise ValueError(
                        "y_true index must be datetime-like or convertible to datetime.") from e

        y_true_baseline = y_true.loc[base_mask] if isinstance(
            y_true, pd.Series) else y_true.squeeze().loc[base_mask]
        y_pred_baseline = pd.Series(np.asarray(
            y_pred).reshape(-1), index=y_true_baseline.index)

        # Projection mask
        proj_mask = _build_mask(projection_period)
        X_proj = df.loc[proj_mask, input_cols]
        y_proj_true = None
        if output_col in df.columns:
            y_proj_true = df.loc[proj_mask, output_col]
        y_proj_pred = None
        if hasattr(model, "predict"):
            try:
                y_proj_pred = pd.Series(np.asarray(
                    model.predict(X_proj)).reshape(-1), index=X_proj.index)
            except Exception:
                y_proj_pred = None

        fig, axes = plt.subplots(1, 2, figsize=self.figsize, sharey=False)
        ax1, ax2 = axes

        # Baseline plot
        ax1.plot(y_true_baseline.index, y_true_baseline.values,
                 label="Actual", color="#1f77b4", linewidth=2)
        ax1.plot(y_pred_baseline.index, y_pred_baseline.values,
                 label="Predicted", color="#ff7f0e", linewidth=2, alpha=0.85)
        ax1.set_title(f"{site} | Baseline\n{model_name} (Adj R2={adj_r2:.3f})")
        ax1.set_xlabel("Date")
        ax1.set_ylabel(output_col if isinstance(output_col, str) else "Target")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Projection plot
        plotted_any = False
        if y_proj_pred is not None:
            ax2.plot(y_proj_pred.index, y_proj_pred.values,
                     label="Projected (Predicted)", color="#d62728", linewidth=2)
            plotted_any = True
        if y_proj_true is not None and len(y_proj_true) > 0:
            ax2.plot(y_proj_true.index, y_proj_true.values,
                     label="Actual", color="#2ca02c", linewidth=2, alpha=0.85)
            plotted_any = True

        ax2.set_title(f"{site} | Projection\n{model_name}")
        ax2.set_xlabel("Date")
        ax2.set_ylabel(output_col if isinstance(output_col, str) else "Target")
        if plotted_any:
            ax2.legend()
        ax2.grid(True, alpha=0.3)

        # Visual shading for periods if they are a single range
        def _maybe_span(ax, period, color, alpha=0.08):
            if isinstance(period, (list, tuple)) and len(period) == 2 and all(isinstance(x, str) for x in period):
                start, end = pd.to_datetime(
                    period[0]), pd.to_datetime(period[1])
                ax.axvspan(start, end, color=color, alpha=alpha)

        _maybe_span(ax1, baseline_period, "#1f77b4")
        _maybe_span(ax2, projection_period, "#d62728")

        plt.tight_layout()
        self.count += 1
        return fig
