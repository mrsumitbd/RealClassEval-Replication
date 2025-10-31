
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score


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
        plt.matshow(data.corr(), fignum=self.count)
        plt.xticks(range(data.shape[1]),
                   data.columns, fontsize=14, rotation=90)
        plt.gca().xaxis.tick_bottom()
        plt.yticks(range(data.shape[1]), data.columns, fontsize=14)
        cb = plt.colorbar()
        cb.ax.tick_params(labelsize=14)
        plt.title('Correlation Matrix', fontsize=14)
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
        plt.figure(self.count, figsize=self.figsize)

        # Plot baseline
        plt.plot(y_true[baseline_period], label='Actual', color='blue')
        plt.plot(y_pred[baseline_period], label='Predicted', color='red')

        # Plot projection
        plt.plot(y_pred[projection_period], label='Projection', color='green')

        plt.title(f'{model_name} - Adjusted R2: {adj_r2:.2f}', fontsize=14)
        plt.xlabel('Date', fontsize=14)
        plt.ylabel(output_col, fontsize=14)
        plt.legend(fontsize=14)
        plt.grid(True)
        plt.show()

        return plt.gcf()
