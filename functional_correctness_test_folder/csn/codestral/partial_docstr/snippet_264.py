
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


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
        self.count += 1
        plt.figure(self.count, figsize=self.figsize)
        sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
        plt.title('Correlation Plot')
        plt.show()

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
        fig, ax = plt.subplots(1, 2, figsize=self.figsize)

        # Baseline plot
        ax[0].plot(y_true[baseline_period], label='Actual')
        ax[0].plot(y_pred[baseline_period], label='Predicted')
        ax[0].set_title(
            f'Baseline Period: {model_name} (Adj. R2: {adj_r2:.2f})')
        ax[0].legend()

        # Projection plot
        ax[1].plot(y_true[projection_period], label='Actual')
        ax[1].plot(y_pred[projection_period], label='Predicted')
        ax[1].set_title(
            f'Projection Period: {model_name} (Adj. R2: {adj_r2:.2f})')
        ax[1].legend()

        plt.tight_layout()
        plt.show()

        return fig
