
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


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
        self.count = 0
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
        self.count += 1
        plt.figure(self.count, figsize=self.figsize)
        corr = data.corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
        plt.title("Pearson's Correlation Heatmap")
        return plt.gcf()

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
        self.count += 1
        plt.figure(self.count, figsize=self.figsize)

        # Plot baseline data
        plt.plot(data.index, data[output_col], label='Actual', color='blue')
        plt.plot(data.index, y_pred, label='Predicted',
                 color='red', linestyle='--')

        # Highlight baseline and projection periods
        plt.axvspan(baseline_period[0], baseline_period[1],
                    color='green', alpha=0.1, label='Baseline Period')
        plt.axvspan(projection_period[0], projection_period[1],
                    color='yellow', alpha=0.1, label='Projection Period')

        plt.title(
            f'{model_name} - Baseline and Projection\nAdjusted R2: {adj_r2:.2f} - Site: {site}')
        plt.xlabel('Date')
        plt.ylabel(output_col)
        plt.legend()
        plt.grid(True)

        return plt.gcf()
