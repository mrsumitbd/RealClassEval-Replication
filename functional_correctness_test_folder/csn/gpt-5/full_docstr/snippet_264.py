import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import AutoDateLocator, AutoDateFormatter


class Plot_Data:
    ''' This class contains functions for displaying various plots.
    Attributes
    ----------
    count    : int
        Keeps track of the number of figures.
    '''

    def __init__(self, figsize=(18, 5)):
        ''' Constructor.
        Parameters
        ----------
        figsize : tuple
            Size of figure.
        '''
        self.figsize = figsize
        self.count = 0
        try:
            sns.set_style("whitegrid")
        except Exception:
            pass

    def correlation_plot(self, data):
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
            data = pd.DataFrame(data)

        num = data.select_dtypes(include=[np.number])
        if num.empty:
            raise ValueError(
                "No numeric columns found for correlation heatmap.")

        corr = num.corr(method='pearson')

        fig, ax = plt.subplots(figsize=self.figsize, constrained_layout=True)
        sns.heatmap(
            corr,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            center=0,
            square=True,
            cbar_kws={"shrink": 0.8},
            ax=ax
        )
        ax.set_title("Pearson Correlation Heatmap", fontsize=12)
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
        # Prepare time index
        if isinstance(data.index, pd.DatetimeIndex):
            x_all = data.index
        elif "date" in data.columns:
            x_all = pd.to_datetime(data["date"])
        else:
            # Fallback to a simple integer index if no date information
            x_all = pd.RangeIndex(start=0, stop=len(data), step=1)

        # Ensure Series alignment
        y_true_series = y_true if isinstance(y_true, pd.Series) else pd.Series(
            y_true, index=x_all[:len(y_true)])
        # y_pred may be array; align later

        def _to_periods(spec):
            # Accept ["start", "end"] or [["s1","e1"], ["s2","e2"], ...]
            if spec is None:
                return []
            if isinstance(spec, (tuple, list)) and len(spec) > 0 and isinstance(spec[0], (list, tuple, pd.Series, np.ndarray)):
                return [(pd.to_datetime(s[0]), pd.to_datetime(s[1])) for s in spec]
            if isinstance(spec, (list, tuple)) and len(spec) >= 2:
                return [(pd.to_datetime(spec[0]), pd.to_datetime(spec[1]))]
            if isinstance(spec, (list, tuple)) and len(spec) == 1:
                start = pd.to_datetime(spec[0])
                return [(start, start)]
            raise ValueError("Invalid period specification.")

        baseline_ranges = _to_periods(baseline_period)
        proj_ranges = _to_periods(projection_period)

        # Build figure with two subplots: Baseline and Projection
        fig, axes = plt.subplots(
            1, 2, figsize=self.figsize, sharey=True, constrained_layout=True)
        ax_base, ax_proj = axes

        # Baseline plot
        if baseline_ranges:
            b_start, b_end = baseline_ranges[0]
            if isinstance(x_all, pd.DatetimeIndex):
                mask_base = (x_all >= b_start) & (x_all <= b_end)
            else:
                # If no datetime axis, assume integer positions mapping by order; approximate via entire range length
                mask_base = pd.Series(
                    [True] * len(x_all), index=np.arange(len(x_all)))
            x_base = x_all[mask_base]

            # Extract y_true for baseline
            if isinstance(y_true_series.index, pd.DatetimeIndex) and isinstance(x_all, pd.DatetimeIndex):
                y_true_base = y_true_series.loc[(y_true_series.index >= b_start) & (
                    y_true_series.index <= b_end)]
                # If selection yields empty but lengths match mask, fallback to positional
                if y_true_base.empty and len(y_true_series) >= mask_base.sum():
                    y_true_base = pd.Series(
                        y_true_series.values[:mask_base.sum()], index=x_base)
            else:
                # Positional alignment
                y_true_base = pd.Series(np.asarray(y_true_series)[
                                        :mask_base.sum()], index=x_base)

            # Align y_pred to baseline
            y_pred = np.asarray(y_pred)
            if len(y_pred) >= len(y_true_base):
                y_pred_base = y_pred[:len(y_true_base)]
            else:
                # Pad with nan if shorter
                pad = np.full(len(y_true_base) - len(y_pred), np.nan)
                y_pred_base = np.concatenate([y_pred, pad])

            ax_base.plot(x_base, y_true_base.values,
                         label="Actual", color="#1f77b4", lw=1.8)
            ax_base.plot(x_base, y_pred_base, label="Predicted",
                         color="#d62728", lw=1.8, alpha=0.9)
            if isinstance(x_all, pd.DatetimeIndex):
                ax_base.axvspan(b_start, b_end, color="#cccccc",
                                alpha=0.2, label="Baseline")
            ax_base.set_title("Baseline")
            ax_base.set_xlabel("Date" if isinstance(
                x_all, pd.DatetimeIndex) else "Index")
            ax_base.set_ylabel(output_col if output_col else "Value")
            ax_base.grid(True, alpha=0.3)
            ax_base.legend(loc="best")
        else:
            ax_base.set_visible(False)

        # Projection plot(s)
        colors = sns.color_palette("tab10", max(1, len(proj_ranges)))
        for i, (p_start, p_end) in enumerate(proj_ranges):
            if isinstance(x_all, pd.DatetimeIndex):
                mask_proj = (x_all >= p_start) & (x_all <= p_end)
            else:
                mask_proj = pd.Series([False] * len(x_all))
            if not mask_proj.any():
                continue

            x_proj = x_all[mask_proj]

            # Actual values for projection if available
            y_actual_proj = None
            if output_col in data.columns:
                y_actual_proj = data.loc[mask_proj, output_col]
                # Ensure it's aligned to x_proj
                if len(y_actual_proj) != len(x_proj):
                    y_actual_proj = pd.Series(
                        y_actual_proj.values[:len(x_proj)], index=x_proj)

            # Model predictions for projection
            y_hat_proj = None
            try:
                X_proj = data.loc[mask_proj, input_col]
                if hasattr(model, "predict"):
                    y_hat_proj = np.asarray(model.predict(X_proj))
                elif callable(model):
                    y_hat_proj = np.asarray(model(X_proj))
                else:
                    y_hat_proj = np.full(len(x_proj), np.nan)
            except Exception:
                y_hat_proj = np.full(len(x_proj), np.nan)

            # Plot
            if y_actual_proj is not None and len(y_actual_proj) > 0:
                ax_proj.plot(x_proj, y_actual_proj.values,
                             color=colors[i], lw=1.6, alpha=0.8, label=f"Actual ({i+1})")
            ax_proj.plot(
                x_proj, y_hat_proj, color=colors[i], lw=2.0, linestyle="--", label=f"Predicted ({i+1})")
            if isinstance(x_all, pd.DatetimeIndex):
                ax_proj.axvspan(p_start, p_end, color=colors[i], alpha=0.12)

        ax_proj.set_title("Projection")
        ax_proj.set_xlabel("Date" if isinstance(
            x_all, pd.DatetimeIndex) else "Index")
        ax_proj.grid(True, alpha=0.3)
        if len(ax_proj.lines) > 0:
            ax_proj.legend(loc="best")

        # Super title
        site_str = f" | Site: {site}" if site is not None else ""
        try:
            score_str = f"{adj_r2:.3f}"
        except Exception:
            score_str = str(adj_r2)
        fig.suptitle(
            f"Model: {model_name} | Adj. R²: {score_str}{site_str}", fontsize=13)

        # Format dates
        if isinstance(x_all, pd.DatetimeIndex):
            for ax in [ax_base, ax_proj]:
                locator = AutoDateLocator()
                formatter = AutoDateFormatter(locator)
                ax.xaxis.set_major_locator(locator)
                ax.xaxis.set_major_formatter(formatter)
                for label in ax.get_xticklabels():
                    label.set_rotation(30)
                    label.set_ha("right")

        self.count += 1
        return fig
