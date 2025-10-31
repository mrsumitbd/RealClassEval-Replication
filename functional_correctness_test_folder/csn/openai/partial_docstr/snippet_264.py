
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


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

    def correlation_plot(self, data):
        """
        Plot a heatmap of the correlation matrix of the provided DataFrame.

        Parameters
        ----------
        data : pd.DataFrame
            DataFrame containing numeric columns.

        Returns
        -------
        matplotlib.figure.Figure
            The correlation heatmap figure.
        """
        corr = data.corr()
        fig, ax = plt.subplots(figsize=self.figsize)
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        ax.set_title("Correlation Matrix")
        self.count += 1
        return fig

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
        """
        Create baseline and projection plots.

        Parameters
        ----------
        y_true              : pd.Series
            Actual y values.
        y_pred              : np.ndarray
            Predicted y values.
        baseline_period     : list(str)
            Baseline period (list of dates or index labels).
        projection_period   : list(str)
            Projection periods (list of dates or index labels).
        model_name          : str
            Optimal model's name.
        adj_r2              : float
            Adjusted R2 score of optimal model.
        data                : pd.DataFrame
            Data containing real values.
        input_col           : list(str)
            Predictor column(s).
        output_col          : str
            Target column.
        model               : func
            Optimal model.
        site                : str
            Site name for title.

        Returns
        -------
        matplotlib.figure.Figure
            Baseline and projection plot figure.
        """
        # Ensure y_true is a Series with a datetime-like index
        if not isinstance(y_true, pd.Series):
            raise TypeError("y_true must be a pandas Series")

        # Create a DataFrame with predictions
        df_pred = pd.DataFrame(
            {
                "y_true": y_true,
                "y_pred": pd.Series(y_pred, index=y_true.index),
            }
        )

        # Filter baseline and projection data
        baseline_mask = df_pred.index.isin(baseline_period)
        projection_mask = df_pred.index.isin(projection_period)

        df_baseline = df_pred.loc[baseline_mask]
        df_projection = df_pred.loc[projection_mask]

        # Create figure with two subplots
        fig, axes = plt.subplots(1, 2, figsize=self.figsize, sharey=True)
        ax_base, ax_proj = axes

        # Baseline plot
        ax_base.plot(df_baseline.index,
                     df_baseline["y_true"], label="Observed", color="black")
        ax_base.plot(
            df_baseline.index, df_baseline["y_pred"], label="Predicted", color="red", linestyle="--")
        ax_base.set_title(
            f"{site} - Baseline ({baseline_period[0]} to {baseline_period[-1]})")
        ax_base.set_xlabel("Date")
        ax_base.set_ylabel(output_col)
        ax_base.legend()
        ax_base.grid(True)

        # Projection plot
        ax_proj.plot(df_projection.index,
                     df_projection["y_true"], label="Observed", color="black")
        ax_proj.plot(df_projection.index,
                     df_projection["y_pred"], label="Predicted", color="red", linestyle="--")
        ax_proj.set_title(
            f"{site} - Projection ({projection_period[0]} to {projection_period[-1]})")
        ax_proj.set_xlabel("Date")
        ax_proj.legend()
        ax_proj.grid(True)

        # Overall title with model info
        fig.suptitle(
            f"{site} - {model_name} (Adj. R² = {adj_r2:.3f})",
            fontsize=16,
            y=0.95,
        )

        fig.tight_layout(rect=[0, 0, 1, 0.93])
        self.count += 1
        return fig
