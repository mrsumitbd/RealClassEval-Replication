
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


class Plot_Data:
    def __init__(self, figsize=(18, 5)):
        """
        Initialize the Plot_Data object.

        Parameters
        ----------
        figsize : tuple, optional
            Size of the figure in inches. Default is (18, 5).
        """
        self.figsize = figsize

    def correlation_plot(self, data):
        """
        Plot a heatmap of the correlation matrix for numeric columns in the DataFrame.

        Parameters
        ----------
        data : pd.DataFrame
            DataFrame containing the data to plot.

        Returns
        -------
        matplotlib.figure.Figure
            The figure containing the correlation heatmap.
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame")

        # Compute correlation matrix for numeric columns only
        corr = data.select_dtypes(include=[np.number]).corr()

        # Create figure
        fig, ax = plt.subplots(figsize=self.figsize)
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax,
                    cbar_kws={"shrink": .8})
        ax.set_title("Correlation Matrix", fontsize=16)
        plt.tight_layout()
        return fig

    def baseline_projection_plot(self,
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
                                 site):
        """
        Plot baseline and projection periods with actual vs predicted values.

        Parameters
        ----------
        y_true : array-like
            True target values.
        y_pred : array-like
            Predicted target values.
        baseline_period : tuple
            (start, end) for baseline period. Can be datetime or index.
        projection_period : tuple
            (start, end) for projection period. Can be datetime or index.
        model_name : str
            Name of the model.
        adj_r2 : float
            Adjusted R² value of the model.
        data : pd.DataFrame
            DataFrame containing the full dataset with a datetime index or a date column.
        input_col : str
            Name of the input column used for predictions.
        output_col : str
            Name of the output column (target).
        model : object
            The fitted model (not used directly in plotting but kept for API consistency).
        site : str
            Site identifier for labeling.

        Returns
        -------
        matplotlib.figure.Figure
            The figure containing the baseline and projection plots.
        """
        # Validate inputs
        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame")

        # Ensure data has a datetime index or a date column
        if isinstance(data.index, pd.DatetimeIndex):
            date_col = data.index
        elif "date" in data.columns:
            date_col = pd.to_datetime(data["date"])
        else:
            raise ValueError(
                "Data must have a datetime index or a 'date' column")

        # Convert y_true and y_pred to pandas Series with the same index
        y_true_series = pd.Series(y_true, index=date_col)
        y_pred_series = pd.Series(y_pred, index=date_col)

        # Create figure with two subplots
        fig, axes = plt.subplots(2, 1, figsize=self.figsize, sharex=True)

        # Baseline plot
        ax_base = axes[0]
        base_mask = (date_col >= baseline_period[0]) & (
            date_col <= baseline_period[1])
        ax_base.plot(
            date_col[base_mask], y_true_series[base_mask], label="Actual", color="black")
        ax_base.plot(date_col[base_mask], y_pred_series[base_mask],
                     label="Predicted", color="red", linestyle="--")
        ax_base.set_title(
            f"Baseline Period ({baseline_period[0]} to {baseline_period[1]})")
        ax_base.set_ylabel(output_col)
        ax_base.legend()
        ax_base.grid(True)

        # Projection plot
        ax_proj = axes[1]
        proj_mask = (date_col >= projection_period[0]) & (
            date_col <= projection_period[1])
        ax_proj.plot(
            date_col[proj_mask], y_true_series[proj_mask], label="Actual", color="black")
        ax_proj.plot(date_col[proj_mask], y_pred_series[proj_mask],
                     label="Predicted", color="red", linestyle="--")
        ax_proj.set_title(
            f"Projection Period ({projection_period[0]} to {projection_period[1]})")
        ax_proj.set_ylabel(output_col)
        ax_proj.legend()
        ax_proj.grid(True)

        # Overall title
        fig.suptitle(
            f"{model_name} at {site} | Adjusted R²: {adj_r2:.3f}", fontsize=18)

        # X-axis label
        axes[-1].set_xlabel("Date")

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        return fig
