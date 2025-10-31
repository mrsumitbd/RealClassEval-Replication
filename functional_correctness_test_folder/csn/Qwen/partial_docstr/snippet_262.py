
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns


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
        self.count += 1
        plt.figure(figsize=self.figsize)
        correlation_matrix = data.corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlation Matrix')
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
        fig, ax = plt.subplots(figsize=self.figsize)

        # Convert baseline and projection periods to datetime if they are not already
        baseline_period = pd.to_datetime(baseline_period)
        projection_period = pd.to_datetime(projection_period)

        # Plot actual values
        ax.plot(data.index, data[output_col], label='Actual', color='blue')

        # Plot baseline predictions
        ax.plot(baseline_period, y_true, label='Baseline Actual',
                linestyle='--', color='green')
        ax.plot(baseline_period, y_pred[:len(
            baseline_period)], label='Baseline Predicted', linestyle='--', color='red')

        # Plot projection predictions
        ax.plot(projection_period, y_pred[len(
            baseline_period):], label='Projection Predicted', linestyle='-', color='orange')

        # Adding titles and labels
        ax.set_title(
            f'{site} - {model_name} Baseline and Projection Plot (Adj R2: {adj_r2:.2f})')
        ax.set_xlabel('Date')
        ax.set_ylabel(output_col)
        ax.legend()

        plt.show()
        return fig
