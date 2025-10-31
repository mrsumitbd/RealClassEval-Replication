
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
        ''' Constructor.
        Parameters
        ----------
        figsize : tuple
            Size of figure.
        '''
        self.figsize = figsize
        self.count = 0

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
        plt.figure(figsize=self.figsize)
        corr = data.corr()
        sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm')
        plt.title('Pearson Correlation Coefficient Heatmap')
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

        # Plotting baseline
        baseline_data = data[(data.index >= baseline_period[0]) & (
            data.index <= baseline_period[1])]
        ax.plot(baseline_data.index,
                baseline_data[output_col], label='Actual (Baseline)', color='blue')
        ax.plot(baseline_data.index, model.predict(
            baseline_data[input_col]), label='Predicted (Baseline)', color='orange', linestyle='--')

        # Plotting projection
        projection_data = data[(data.index >= projection_period[0]) & (
            data.index <= projection_period[1])]
        ax.plot(projection_data.index,
                projection_data[output_col], label='Actual (Projection)', color='green')
        ax.plot(projection_data.index, y_pred,
                label='Predicted (Projection)', color='red', linestyle='--')

        ax.set_title(
            f'{site} - Baseline and Projection Plot\nModel: {model_name}, Adjusted R2: {adj_r2:.2f}')
        ax.set_xlabel('Date')
        ax.set_ylabel(output_col)
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
