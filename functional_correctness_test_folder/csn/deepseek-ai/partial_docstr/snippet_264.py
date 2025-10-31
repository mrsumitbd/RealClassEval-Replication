
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
        sns.heatmap(data.corr(), annot=True, cmap='coolwarm', center=0)
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
        plt.figure(self.count, figsize=self.figsize)

        # Plot baseline data
        plt.plot(y_true.index, y_true, label='Actual', color='blue')
        plt.plot(y_true.index, y_pred, label='Predicted',
                 color='red', linestyle='--')

        # Plot projection data if available
        if projection_period:
            proj_data = data[projection_period[0]:projection_period[1]]
            X_proj = proj_data[input_col]
            y_proj = proj_data[output_col]
            y_proj_pred = model.predict(X_proj)

            plt.plot(y_proj.index, y_proj,
                     label='Actual (Projection)', color='green')
            plt.plot(y_proj.index, y_proj_pred,
                     label='Predicted (Projection)', color='orange', linestyle='--')

        plt.axvline(x=baseline_period[1], color='black',
                    linestyle=':', label='Baseline End')
        plt.title(f'{model_name} - {site}\nAdjusted R2: {adj_r2:.2f}')
        plt.legend()
        plt.grid()
        plt.show()
