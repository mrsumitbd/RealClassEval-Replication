import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


class Plot_Data:

    def __init__(self, figsize=(18, 5)):
        self.figsize = figsize
        sns.set_style("whitegrid")

    def correlation_plot(self, data):
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data)
        corr = data.corr(numeric_only=True)
        fig, ax = plt.subplots(figsize=self.figsize)
        sns.heatmap(
            corr,
            ax=ax,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            center=0,
            square=True,
            cbar_kws={"shrink": 0.8, "label": "Correlation"},
        )
        ax.set_title("Correlation Matrix")
        plt.tight_layout()
        return fig, ax

    def baseline_projection_plot(
        self,
        y_true,
        y_pred,
        baseline_period,
        projection_period,
        model_name,
        adj_r2,
        data,
        input_col,
        output_col,
        model,
        site,
    ):
        def _as_series(arr, index=None, name=None):
            if isinstance(arr, pd.Series):
                s = arr.copy()
            else:
                s = pd.Series(arr, index=index)
            if name is not None:
                s.name = name
            return s

        def _normalize_periods(period):
            if period is None:
                return []
            # Allow (start, end), list/tuple of pairs
            if isinstance(period, (tuple, list)) and len(period) == 2 and not isinstance(period[0], (list, tuple)):
                periods = [period]
            else:
                periods = list(period)
            norm = []
            for p in periods:
                if p is None:
                    continue
                start = pd.to_datetime(p[0])
                end = pd.to_datetime(p[1])
                if pd.isna(start) or pd.isna(end):
                    continue
                if end < start:
                    start, end = end, start
                norm.append((start, end))
            return norm

        # Prepare data/index alignment
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data)
        index = data.index
        y_true = _as_series(y_true, index=index, name="Observed")
        y_pred = _as_series(y_pred, index=index, name="Predicted")

        df = pd.concat([y_true, y_pred], axis=1).dropna()
        if df.empty:
            raise ValueError(
                "No overlapping non-NaN data found between y_true and y_pred.")

        # Metrics
        r2 = r2_score(df["Observed"], df["Predicted"])
        mae = mean_absolute_error(df["Observed"], df["Predicted"])
        rmse = mean_squared_error(
            df["Observed"], df["Predicted"], squared=False)

        # Plot
        fig, axes = plt.subplots(1, 2, figsize=self.figsize)

        # Left: Predicted vs Observed scatter
        ax0 = axes[0]
        sns.scatterplot(
            x=df["Observed"],
            y=df["Predicted"],
            ax=ax0,
            s=30,
            color="#2a9d8f",
            edgecolor="white",
            alpha=0.8,
        )
        mn = np.nanmin([df["Observed"].min(), df["Predicted"].min()])
        mx = np.nanmax([df["Observed"].max(), df["Predicted"].max()])
        ax0.plot([mn, mx], [mn, mx], ls="--",
                 c="#264653", lw=1.5, label="1:1 line")
        ax0.set_xlabel(f"Observed ({output_col})")
        ax0.set_ylabel(f"Predicted ({output_col})")
        ax0.set_title(f"{model_name} — Predicted vs Observed")
        ax0.legend(loc="best")

        metrics_text = (
            f"Site: {site}\n"
            f"R²: {r2:.3f}\n"
            f"Adj. R²: {adj_r2:.3f}\n"
            f"RMSE: {rmse:.3f}\n"
            f"MAE: {mae:.3f}"
        )
        ax0.text(
            0.05,
            0.95,
            metrics_text,
            transform=ax0.transAxes,
            va="top",
            ha="left",
            bbox=dict(boxstyle="round,pad=0.3", fc="white",
                      ec="lightgray", alpha=0.9),
            fontsize=9,
        )

        # Right: Time series with baseline/projection shading
        ax1 = axes[1]
        df.sort_index(inplace=True)
        ax1.plot(df.index, df["Observed"],
                 label="Observed", color="#1f77b4", lw=1.5)
        ax1.plot(df.index, df["Predicted"], label="Predicted",
                 color="#d62728", lw=1.5, alpha=0.9)
        ax1.set_title(f"{model_name} — Time Series\nSite: {site}")
        ax1.set_xlabel("Time")
        ax1.set_ylabel(output_col)
        ax1.legend(loc="best")

        baseline_periods = _normalize_periods(baseline_period)
        projection_periods = _normalize_periods(projection_period)

        def _shade(ax, periods, color, label):
            first = True
            for (start, end) in periods:
                ax.axvspan(start, end, color=color, alpha=0.15,
                           label=label if first else None)
                first = False

        _shade(ax1, baseline_periods, "#2ca02c", "Baseline")
        _shade(ax1, projection_periods, "#ff7f0e", "Projection")

        # Try to mark transition if contiguous and non-overlapping
        all_marks = []
        for (s, e) in baseline_periods + projection_periods:
            all_marks.extend([s, e])
        for t in sorted(set(all_marks)):
            if df.index.min() <= t <= df.index.max():
                ax1.axvline(t, color="k", lw=0.7, ls=":")

        plt.tight_layout()
        return fig, axes
