
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

        # Assume data has a datetime index or a column named 'date' or similar
        if 'date' in data.columns:
            x_axis = pd.to_datetime(data['date'])
        elif data.index.name is not None and 'date' in data.index.name.lower():
            x_axis = pd.to_datetime(data.index)
        else:
            x_axis = np.arange(len(data))

        # Prepare mask for baseline and projection periods
        if isinstance(x_axis, pd.Series) or isinstance(x_axis, pd.DatetimeIndex):
            baseline_mask = (x_axis >= pd.to_datetime(baseline_period[0])) & (
                x_axis <= pd.to_datetime(baseline_period[1]))
            projection_mask = (x_axis >= pd.to_datetime(projection_period[0])) & (
                x_axis <= pd.to_datetime(projection_period[1]))
        else:
            # fallback: use indices
            baseline_mask = np.zeros(len(x_axis), dtype=bool)
            projection_mask = np.zeros(len(x_axis), dtype=bool)
            baseline_mask[baseline_period[0]:baseline_period[1]+1] = True
            projection_mask[projection_period[0]:projection_period[1]+1] = True

        fig, ax = plt.subplots(figsize=self.figsize)

        # Plot actual values
        ax.plot(x_axis, y_true, label='Actual', color='black', linewidth=2)

        # Plot predicted values
        ax.plot(x_axis, y_pred, label='Predicted',
                color='red', linestyle='--', linewidth=2)

        # Highlight baseline and projection periods
        if isinstance(x_axis, (pd.Series, pd.DatetimeIndex)):
            ax.axvspan(pd.to_datetime(baseline_period[0]), pd.to_datetime(
                baseline_period[1]), color='green', alpha=0.1, label='Baseline')
            ax.axvspan(pd.to_datetime(projection_period[0]), pd.to_datetime(
                projection_period[1]), color='blue', alpha=0.1, label='Projection')
        else:
            ax.axvspan(baseline_period[0], baseline_period[1],
                       color='green', alpha=0.1, label='Baseline')
            ax.axvspan(projection_period[0], projection_period[1],
                       color='blue', alpha=0.1, label='Projection')

        ax.set_title(f"{site} - {model_name} (Adj R2: {adj_r2:.3f})")
        ax.set_xlabel("Date" if (isinstance(
            x_axis, (pd.Series, pd.DatetimeIndex))) else "Index")
        ax.set_ylabel(output_col)
        ax.legend()
        plt.tight_layout()
        return fig
