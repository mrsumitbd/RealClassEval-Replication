
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
            Size of the figures to be created. Default is (18, 5).
        """
        self.figsize = figsize

    def correlation_plot(self, data):
        """
        Plot a heatmap of the correlation matrix of the provided DataFrame.

        Parameters
        ----------
        data : pandas.DataFrame
            DataFrame containing numeric columns to compute correlations.
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError("`data` must be a pandas DataFrame")

        corr = data.corr()
        plt.figure(figsize=self.figsize)
        sns.heatmap(
            corr,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            square=True,
            cbar_kws={"shrink": 0.8}
        )
        plt.title("Correlation Matrix", fontsize=16)
        plt.tight_layout()
        plt.show()

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
        site
    ):
        """
        Plot observed vs predicted values with baseline and projection periods shaded.

        Parameters
        ----------
        y_true : array-like or pandas.Series
            Observed target values.
        y_pred : array-like or pandas.Series
            Predicted target values.
        baseline_period : tuple
            (start, end) dates for the baseline period.
        projection_period : tuple
            (start, end) dates for the projection period.
        model_name : str
            Name of the model used.
        adj_r2 : float
            Adjusted R² value of the model.
        data : pandas.DataFrame
            DataFrame containing the time index or a 'date' column.
        input_col : str
            Label for the x‑axis (typically the time variable).
        output_col : str
            Label for the y‑axis (target variable).
        model : object
            The model object (used only for its string representation).
        site : str
            Site or location name.
        """
        # Validate inputs
        if not isinstance(data, pd.DataFrame):
            raise TypeError("`data` must be a pandas DataFrame")

        # Determine time axis
        if isinstance(data.index, pd.DatetimeIndex):
            time = data.index
        elif "date" in data.columns:
            time = pd.to_datetime(data["date"])
        else:
            # Fallback: use integer index
            time = np.arange(len(y_true))

        # Ensure y_true and y_pred are pandas Series with the same index
        if not isinstance(y_true, pd.Series):
            y_true = pd.Series(y_true, index=time)
        if not isinstance(y_pred, pd.Series):
            y_pred = pd.Series(y_pred, index=time)

        # Create figure
        plt.figure(figsize=self.figsize)

        # Plot observed and predicted
        plt.plot(time, y_true, label="Observed", color="black", linewidth=2)
        plt.plot(time, y_pred, label="Predicted",
                 color="red", linestyle="--", linewidth=2)

        # Shade baseline period
        baseline_start, baseline_end = baseline_period
        baseline_start_ts = pd.to_datetime(baseline_start)
        baseline_end_ts = pd.to_datetime(baseline_end)
        plt.axvspan(
            baseline_start_ts,
            baseline_end_ts,
            color="blue",
            alpha=0.1,
            label="Baseline Period",
        )

        # Shade projection period
        proj_start, proj_end = projection_period
        proj_start_ts = pd.to_datetime(proj_start)
        proj_end_ts = pd.to_datetime(proj_end)
        plt.axvspan(
            proj_start_ts,
            proj_end_ts,
            color="green",
            alpha=0.1,
            label="Projection Period",
        )

        # Title and labels
        title = (
            f"{site} - {model_name} (Adj R² = {adj_r2:.3f})"
            f"\nModel: {model}"
        )
        plt.title(title, fontsize=14, pad=20)
        plt.xlabel(input_col, fontsize=12)
        plt.ylabel(output_col, fontsize=12)

        # Legend
        plt.legend(loc="upper left", fontsize=10)

        # Layout and show
        plt.tight_layout()
        plt.show()
