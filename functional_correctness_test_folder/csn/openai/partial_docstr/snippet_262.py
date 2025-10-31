
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

    def baseline_projection_plot(self, y_true, y_pred, baseline_period, projection_period,
                                 model_name, adj_r2, data, input_col, output_col, model, site):
        """
        Create baseline and projection plots.
        Parameters
        ----------
        y_true              : pd.Series
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
        data                : pd.DataFrame
            Data containing real values.
        input_col           : list(str)
            Predictor column(s).
        output_col          : str
            Target column.
        model               : func
            Optimal model.
        site                : str
            Site name or identifier.
        Returns
        -------
        matplotlib.figure.Figure
            Baseline plot
        """
        # Ensure y_true is a Series with datetime index
        if not isinstance(y_true, pd.Series):
            y_true = pd.Series(y_true, index=data.index)
        # Create a DataFrame for predictions
        pred_df = pd.DataFrame(
            {'y_true': y_true, 'y_pred': y_pred}, index=data.index)

        # Filter baseline and projection periods
        baseline_mask = pred_df.index.isin(baseline_period)
        projection_mask = pred_df.index.isin(projection_period)

        fig, ax = plt.subplots(figsize=self.figsize)
        # Plot baseline
        ax.plot(pred_df.index[baseline_mask], pred_df.loc[baseline_mask, 'y_true'],
                label='Baseline Actual', color='blue')
        ax.plot(pred_df.index[baseline_mask], pred_df.loc[baseline_mask, 'y_pred'],
                label='Baseline Predicted', color='cyan', linestyle='--')
        # Plot projection
        ax.plot(pred_df.index[projection_mask], pred_df.loc[projection_mask, 'y_true'],
                label='Projection Actual', color='red')
        ax.plot(pred_df.index[projection_mask], pred_df.loc[projection_mask, 'y_pred'],
                label='Projection Predicted', color='orange', linestyle='--')

        ax.set_title(f'{site} - {model_name} (Adj R² = {adj_r2:.3f})')
        ax.set_xlabel('Date')
        ax.set_ylabel(output_col)
        ax.legend()
        ax.grid(True)
        self.count += 1
        return fig
