
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
        self.count = 0
        self.figsize = figsize

    def correlation_plot(self, data):
        plt.figure(figsize=self.figsize)
        self.count += 1
        sns.heatmap(data.corr(), annot=True, cmap='coolwarm', square=True)
        plt.title('Correlation Plot')
        plt.show()

    def baseline_projection_plot(self, y_true, y_pred, baseline_period, projection_period, model_name, adj_r2, data, input_col, output_col, model):
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
        fig, ax = plt.subplots(1, 2, figsize=(
            self.figsize[0]*2, self.figsize[1]))
        self.count += 1

        # Baseline plot
        baseline_mask = (data.index >= baseline_period[0]) & (
            data.index <= baseline_period[1])
        ax[0].plot(y_true[baseline_mask], label='Actual')
        ax[0].plot(y_pred[baseline_mask], label='Predicted')
        ax[0].set_title(
            f'Baseline Period: {baseline_period[0]} to {baseline_period[1]}')
        ax[0].set_xlabel('Time')
        ax[0].set_ylabel(output_col)
        ax[0].legend()

        # Projection plot
        projection_mask = (data.index >= projection_period[0]) & (
            data.index <= projection_period[1])
        ax[1].plot(y_true[projection_mask], label='Actual')
        ax[1].plot(y_pred[projection_mask], label='Predicted')
        ax[1].set_title(
            f'Projection Period: {projection_period[0]} to {projection_period[1]}')
        ax[1].set_xlabel('Time')
        ax[1].set_ylabel(output_col)
        ax[1].legend()

        fig.suptitle(f'{model_name} Model - Adj R2: {adj_r2:.2f}')
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()
        return fig
