import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter


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

    def _get_datetime_index(self, data: pd.DataFrame):
        if isinstance(data.index, pd.DatetimeIndex):
            return data.index, None
        # Try common datetime column names
        for col in ["date", "Date", "datetime", "Datetime", "time", "Time", "timestamp", "Timestamp"]:
            if col in data.columns:
                idx = pd.to_datetime(data[col], errors="coerce")
                return idx, col
        # Fallback: create a range index as time axis
        return pd.RangeIndex(start=0, stop=len(data)), None

    def _to_periods(self, period):
        # Normalize period(s) to list of (start, end) tuples as Timestamps or None
        if period is None:
            return []
        if isinstance(period, (list, tuple)) and len(period) > 0 and not isinstance(period[0], (list, tuple)):
            # Single period provided as [start, end]
            period = [period]
        norm = []
        for p in period:
            if p is None or len(p) == 0:
                continue
            if len(p) == 1:
                start = pd.to_datetime(p[0], errors="coerce")
                end = None
            else:
                start = pd.to_datetime(p[0], errors="coerce")
                end = pd.to_datetime(p[1], errors="coerce")
            norm.append((start, end))
        return norm

    def correlation_plot(self, data):
        # Compute correlation matrix on numeric columns only
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data)
        num_df = data.select_dtypes(include=[np.number])
        if num_df.shape[1] == 0:
            raise ValueError(
                "No numeric columns available to compute correlation.")
        corr = num_df.corr()

        fig, ax = plt.subplots(figsize=self.figsize)
        cax = ax.imshow(corr.values, cmap="coolwarm",
                        vmin=-1, vmax=1, aspect="auto")
        ax.set_xticks(np.arange(corr.shape[1]))
        ax.set_yticks(np.arange(corr.shape[1]))
        ax.set_xticklabels(corr.columns, rotation=45, ha="right")
        ax.set_yticklabels(corr.columns)
        for (i, j), val in np.ndenumerate(corr.values):
            ax.text(j, i, f"{val:.2f}", ha="center",
                    va="center", color="black", fontsize=8)
        ax.set_title("Correlation Matrix")
        fig.colorbar(cax, ax=ax, fraction=0.046, pad=0.04, label="Correlation")
        fig.tight_layout()
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
            raise ValueError("data must be a pandas DataFrame.")
        if isinstance(input_col, str):
            input_col = [input_col]

        time_index, time_col = self._get_datetime_index(data)
        # If we found a time column, align data index temporarily
        df = data.copy()
        df_index = time_index
        # Normalize baseline and projection periods
        baseline_periods = self._to_periods(baseline_period)
        proj_periods = self._to_periods(projection_period)

        # Determine baseline mask
        if len(baseline_periods) == 0:
            base_mask = pd.Series(True, index=np.arange(len(df)))
        else:
            base_mask = pd.Series(False, index=np.arange(len(df)))
            for start, end in baseline_periods:
                if start is None and end is None:
                    base_mask |= True
                elif start is None:
                    base_mask |= (df_index <= end)
                elif end is None:
                    base_mask |= (df_index >= start)
                else:
                    base_mask |= (df_index >= start) & (df_index <= end)

        df_base = df.loc[base_mask.values].copy()
        t_base = df_index[base_mask.values]

        # Prepare baseline y_true and y_pred
        y_true_base = None
        y_pred_base = None

        if y_true is not None:
            if isinstance(y_true, (pd.Series, pd.DataFrame)):
                y_true_arr = np.asarray(y_true).ravel()
            else:
                y_true_arr = np.asarray(y_true).ravel()
        else:
            y_true_arr = None

        if y_pred is not None:
            y_pred_arr = np.asarray(y_pred).ravel()
        else:
            y_pred_arr = None

        # Use provided y_true/y_pred if lengths match baseline selection
        if y_true_arr is not None and len(y_true_arr) == len(df_base):
            y_true_base = y_true_arr
        else:
            if output_col in df_base.columns:
                y_true_base = df_base[output_col].to_numpy()

        if y_pred_arr is not None and len(y_pred_arr) == len(df_base):
            y_pred_base = y_pred_arr
        else:
            # Compute predictions from model if possible
            if model is not None and len(input_col) > 0 and all(c in df_base.columns for c in input_col):
                try:
                    Xb = df_base[input_col].to_numpy()
                    y_pred_base = np.asarray(model.predict(Xb)).ravel()
                except Exception:
                    y_pred_base = None

        # Projection predictions
        # list of dicts: {'t': time, 'y_true': ..., 'y_pred': ...}
        proj_results = []
        for (start, end) in proj_periods:
            if start is None and end is None:
                p_mask = pd.Series(True, index=np.arange(len(df)))
            elif start is None:
                p_mask = (df_index <= end)
            elif end is None:
                p_mask = (df_index >= start)
            else:
                p_mask = (df_index >= start) & (df_index <= end)

            df_p = df.loc[p_mask.values].copy()
            t_p = df_index[p_mask.values]
            y_true_p = df_p[output_col].to_numpy(
            ) if output_col in df_p.columns else None
            y_pred_p = None
            if model is not None and len(df_p) > 0 and len(input_col) > 0 and all(c in df_p.columns for c in input_col):
                try:
                    Xp = df_p[input_col].to_numpy()
                    y_pred_p = np.asarray(model.predict(Xp)).ravel()
                except Exception:
                    y_pred_p = None
            proj_results.append(
                {"t": t_p, "y_true": y_true_p, "y_pred": y_pred_p, "period": (start, end)})

        # Create figure with two subplots: baseline and projection
        fig, axes = plt.subplots(1, 2, figsize=self.figsize, sharey=False)
        ax_base, ax_proj = axes

        # Baseline plot
        if y_true_base is not None and len(t_base) == len(y_true_base):
            ax_base.plot(t_base, y_true_base, label="Actual",
                         color="#1f77b4", linewidth=2)
        if y_pred_base is not None and len(t_base) == len(y_pred_base):
            ax_base.plot(t_base, y_pred_base, label="Predicted",
                         color="#ff7f0e", linewidth=2, alpha=0.9)
        ax_base.set_title("Baseline")
        ax_base.set_xlabel("Time")
        ax_base.set_ylabel(output_col if output_col is not None else "Target")
        ax_base.legend()
        if isinstance(t_base, pd.DatetimeIndex):
            ax_base.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
            fig.autofmt_xdate(rotation=30)

        # Projection plot
        colors = ["#2ca02c", "#d62728", "#9467bd", "#8c564b",
                  "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
        for i, res in enumerate(proj_results):
            t_p = res["t"]
            y_true_p = res["y_true"]
            y_pred_p = res["y_pred"]
            label_suffix = ""
            s, e = res["period"]
            if pd.notna(s) or pd.notna(e):
                s_str = s.strftime("%Y-%m-%d") if isinstance(s,
                                                             pd.Timestamp) and not pd.isna(s) else ""
                e_str = e.strftime("%Y-%m-%d") if isinstance(e,
                                                             pd.Timestamp) and not pd.isna(e) else ""
                if s_str or e_str:
                    label_suffix = f" [{s_str} to {e_str}]"
            if y_true_p is not None and len(t_p) == len(y_true_p):
                ax_proj.plot(t_p, y_true_p, color="#555555", linestyle="--",
                             linewidth=1.5, label=f"Actual{label_suffix}" if i == 0 else None)
            if y_pred_p is not None and len(t_p) == len(y_pred_p):
                ax_proj.plot(t_p, y_pred_p, color=colors[i % len(
                    colors)], linewidth=2, label=f"Predicted{label_suffix}")
        ax_proj.set_title("Projection")
        ax_proj.set_xlabel("Time")
        ax_proj.set_ylabel(output_col if output_col is not None else "Target")
        ax_proj.legend()
        if len(proj_results) > 0 and isinstance(proj_results[0]["t"], pd.DatetimeIndex):
            ax_proj.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
            fig.autofmt_xdate(rotation=30)

        # Overall title
        title_parts = []
        if site:
            title_parts.append(f"Site: {site}")
        if model_name:
            title_parts.append(f"Model: {model_name}")
        if adj_r2 is not None:
            try:
                title_parts.append(f"Adj R2: {float(adj_r2):.3f}")
            except Exception:
                title_parts.append(f"Adj R2: {adj_r2}")
        fig.suptitle(" | ".join(title_parts), fontsize=14, y=1.02)
        fig.tight_layout()
        self.count += 1
        return fig
