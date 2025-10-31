
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

    count = 0

    def __init__(self, figsize=(18, 5)):
        ''' Constructor.
        Parameters
        ----------
        figsize : tuple
            Size of figure.
        '''
        self.figsize = figsize

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
        Plot_Data.count += 1
        corr = data.corr()
        fig, ax = plt.subplots(figsize=self.figsize)
        sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm',
                    ax=ax, square=True, cbar=True)
        ax.set_title("Correlation Matrix Heatmap")
        plt.tight_layout()
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
        Plot_Data.count += 1

        # Prepare time index
        if hasattr(data, 'index') and isinstance(data.index, pd.DatetimeIndex):
            time = data.index
        elif 'date' in data.columns:
            time = pd.to_datetime(data['date'])
        else:
            time = np.arange(len(data))

        # Prepare baseline and projection masks
        baseline_mask = data.index.astype(str).isin(baseline_period)
        projection_mask = data.index.astype(str).isin(projection_period)

        # If periods are not index, try to match with a 'date' column if present
        if not baseline_mask.any() and 'date' in data.columns:
            baseline_mask = data['date'].astype(str).isin(baseline_period)
            projection_mask = data['date'].astype(str).isin(projection_period)

        # Prepare figure
        fig, ax = plt.subplots(figsize=self.figsize)

        # Plot actual values
        ax.plot(time, y_true, label='Actual', color='black', linewidth=2)

        # Plot predicted values
        ax.plot(time, y_pred, label='Predicted',
                color='red', linestyle='--', linewidth=2)

        # Highlight baseline and projection periods
        if baseline_mask.any():
            ax.axvspan(time[baseline_mask][0], time[baseline_mask]
                       [-1], color='green', alpha=0.1, label='Baseline Period')
        if projection_mask.any():
            ax.axvspan(time[projection_mask][0], time[projection_mask]
                       [-1], color='blue', alpha=0.1, label='Projection Period')

        # Title and labels
        title = f"{site} - {model_name} Baseline & Projection\nAdj R2: {adj_r2:.3f}"
        ax.set_title(title)
        ax.set_xlabel("Time")
        ax.set_ylabel(output_col)
        ax.legend()
        plt.tight_layout()
        return fig
