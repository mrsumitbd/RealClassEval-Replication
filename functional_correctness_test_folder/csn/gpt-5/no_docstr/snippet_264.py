import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import gridspec
from typing import Optional, Sequence, Tuple, Union


class Plot_Data:
    def __init__(self, figsize: Tuple[int, int] = (18, 5)):
        self.figsize = figsize
        try:
            sns.set_style("whitegrid")
        except Exception:
            pass

    def correlation_plot(self, data: Union[pd.DataFrame, np.ndarray, dict]):
        if isinstance(data, dict):
            data = pd.DataFrame(data)
        elif isinstance(data, np.ndarray):
            data = pd.DataFrame(data)

        if not isinstance(data, pd.DataFrame):
            raise TypeError(
                "data must be a pandas DataFrame, numpy array, or dict-like.")

        if data.empty:
            raise ValueError("data is empty.")

        corr = data.corr(numeric_only=True)

        fig, ax = plt.subplots(figsize=self.figsize)
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
                    square=True, cbar=True, ax=ax)
        ax.set_title("Correlation Matrix")
        fig.tight_layout()
        return fig, ax

    def baseline_projection_plot(
        self,
        y_true: Union[pd.Series, np.ndarray],
        y_pred: Union[pd.Series, np.ndarray],
        baseline_period: Optional[Tuple[Union[str, pd.Timestamp], Union[str, pd.Timestamp]]],
        projection_period: Optional[Tuple[Union[str, pd.Timestamp], Union[str, pd.Timestamp]]],
        model_name: str,
        adj_r2: float,
        data: pd.DataFrame,
        input_col: Optional[Sequence[str]],
        output_col: str,
        model,
        site: Optional[str] = None,
    ):
        def _to_ts(v):
            if v is None:
                return None
            if isinstance(v, (pd.Timestamp, np.datetime64)):
                return pd.Timestamp(v)
            return pd.to_datetime(v, errors="coerce")

        if isinstance(data, pd.Series):
            data = data.to_frame(name=output_col)

        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame.")

        if output_col not in data.columns:
            raise ValueError(f"output_col '{output_col}' not found in data.")

        # Prepare index and alignment
        x_index = data.index
        if not isinstance(x_index, (pd.DatetimeIndex, pd.PeriodIndex)):
            # Try to convert to datetime if possible
            try:
                x_index = pd.to_datetime(x_index, errors="coerce")
            except Exception:
                pass

        # Align y_true and y_pred to data index if they are Series with their own index
        def _align_to_data(series_like):
            if isinstance(series_like, pd.Series):
                return series_like.reindex(data.index)
            arr = np.asarray(series_like).reshape(-1)
            if len(arr) != len(data):
                raise ValueError(
                    "Length of y arrays must match length of data when not pandas Series.")
            return pd.Series(arr, index=data.index)

        y_true_s = _align_to_data(y_true)
        y_pred_s = _align_to_data(y_pred)

        # Define periods
        b_start = _to_ts(baseline_period[0]) if baseline_period else None
        b_end = _to_ts(baseline_period[1]) if baseline_period else None
        p_start = _to_ts(projection_period[0]) if projection_period else None
        p_end = _to_ts(projection_period[1]) if projection_period else None

        # Build masks
        idx = pd.Index(x_index)
        if isinstance(idx, pd.DatetimeIndex):
            b_mask = pd.Series(True, index=idx)
            p_mask = pd.Series(False, index=idx)

            if b_start is not None:
                b_mask &= idx >= b_start
            if b_end is not None:
                b_mask &= idx <= b_end

            if p_start is not None:
                p_mask |= idx >= p_start
            if p_end is not None:
                p_mask &= idx <= p_end if p_mask.any() else (idx <= p_end)

            # If projection not given, infer as not baseline
            if projection_period is None:
                p_mask = ~b_mask
        else:
            # Non-datetime index: use full baseline, empty projection by default
            b_mask = pd.Series(True, index=idx)
            p_mask = pd.Series(False, index=idx)

        # Determine if we can compute feature importance
        feature_importances = None
        feature_names = None
        if input_col is not None:
            feature_names = list(input_col)
            if hasattr(model, "feature_importances_"):
                try:
                    vals = np.asarray(model.feature_importances_).reshape(-1)
                    if len(vals) == len(feature_names):
                        feature_importances = vals
                except Exception:
                    pass
            elif hasattr(model, "coef_"):
                try:
                    coef = np.asarray(model.coef_)
                    if coef.ndim > 1:
                        coef = coef.ravel()
                    if len(coef) == len(feature_names):
                        feature_importances = np.abs(coef)
                except Exception:
                    pass

        # Layout
        if feature_importances is None:
            ncols = 2
            width_ratios = [2.5, 1.5]
        else:
            ncols = 3
            width_ratios = [2.5, 1.2, 1.3]

        fig = plt.figure(figsize=self.figsize)
        gs = gridspec.GridSpec(
            1, ncols, width_ratios=width_ratios, figure=fig, wspace=0.25)

        # Time series plot
        ax_ts = fig.add_subplot(gs[0, 0])

        # Actuals
        ax_ts.plot(x_index, data[output_col],
                   color="black", linewidth=1.2, label="Actual")

        # Predictions on baseline
        if b_mask.any():
            ax_ts.plot(x_index[b_mask], y_pred_s[b_mask], color="#1f77b4",
                       linewidth=1.5, label="Predicted (baseline)")

        # Predictions on projection
        if p_mask.any():
            ax_ts.plot(x_index[p_mask], y_pred_s[p_mask], color="#d62728",
                       linewidth=1.5, linestyle="--", label="Predicted (projection)")

        # Shading
        def _shade(ax, mask, color, label):
            if not mask.any():
                return
            # Find contiguous intervals
            m = mask.astype(int).values
            idx_arr = np.arange(len(mask))
            starts = []
            ends = []
            in_block = False
            for i, val in enumerate(m):
                if val and not in_block:
                    in_block = True
                    starts.append(i)
                if in_block and (i == len(m) - 1 or not m[i + 1]):
                    ends.append(i)
                    in_block = False
            for s, e in zip(starts, ends):
                ax.axvspan(x_index[s], x_index[e],
                           color=color, alpha=0.08, label=label)
                label = None  # only label first patch

        _shade(ax_ts, b_mask, "#1f77b4", "Baseline period")
        _shade(ax_ts, p_mask, "#d62728", "Projection period")

        title_site = f" | Site: {site}" if site else ""
        ax_ts.set_title(f"{model_name}{title_site} | Adj R^2 = {adj_r2:.3f}")
        ax_ts.set_xlabel("Time")
        ax_ts.set_ylabel(output_col)
        ax_ts.legend(loc="best")
        ax_ts.grid(True, alpha=0.3)

        # Parity plot
        ax_par = fig.add_subplot(gs[0, 1])
        ax_par.scatter(y_true_s, y_pred_s, s=14, alpha=0.6,
                       color="#2ca02c", edgecolor="none", label="Samples")
        min_v = np.nanmin([np.nanmin(y_true_s.values),
                          np.nanmin(y_pred_s.values)])
        max_v = np.nanmax([np.nanmax(y_true_s.values),
                          np.nanmax(y_pred_s.values)])
        if np.isfinite(min_v) and np.isfinite(max_v):
            pad = 0.02 * (max_v - min_v if max_v > min_v else 1.0)
            ax_par.plot([min_v - pad, max_v + pad], [min_v - pad, max_v + pad],
                        color="black", linestyle="--", linewidth=1, label="1:1")
            ax_par.set_xlim(min_v - pad, max_v + pad)
            ax_par.set_ylim(min_v - pad, max_v + pad)

        # Metrics
        with np.errstate(invalid="ignore"):
            resid = y_true_s.values - y_pred_s.values
            rmse = float(np.sqrt(np.nanmean(resid**2)))
            mae = float(np.nanmean(np.abs(resid)))
            # Unadjusted R^2 for parity scatter
            y_mean = np.nanmean(y_true_s.values)
            ss_tot = np.nansum((y_true_s.values - y_mean) ** 2)
            ss_res = np.nansum(resid ** 2)
            r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan

        ax_par.set_title("Parity Plot")
        ax_par.set_xlabel("Observed")
        ax_par.set_ylabel("Predicted")
        ax_par.legend(loc="best")
        txt = f"R²={r2:.3f}\nRMSE={rmse:.3f}\nMAE={mae:.3f}\nAdj R²={adj_r2:.3f}"
        ax_par.text(0.05, 0.95, txt, transform=ax_par.transAxes, va="top", ha="left",
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7, edgecolor="gray"))

        axes = {"time_series": ax_ts, "parity": ax_par}

        # Feature importances
        if feature_importances is not None and feature_names is not None and len(feature_importances) == len(feature_names):
            ax_imp = fig.add_subplot(gs[0, 2])
            order = np.argsort(feature_importances)
            fi_sorted = feature_importances[order]
            fn_sorted = [feature_names[i] for i in order]
            ax_imp.barh(fn_sorted, fi_sorted, color="#9467bd", alpha=0.9)
            ax_imp.set_title("Feature Importance")
            ax_imp.set_xlabel("Importance")
            fig.tight_layout()
            axes["feature_importance"] = ax_imp
        else:
            fig.tight_layout()

        return fig, axes
