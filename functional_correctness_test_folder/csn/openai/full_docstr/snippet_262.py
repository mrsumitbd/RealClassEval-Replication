
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
        corr = data.corr(method='pearson')
        fig, ax = plt.subplots(figsize=self.figsize)
        sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
        ax.set_title('Pearson Correlation Heatmap')
        self.count += 1
        return fig

    def baseline_projection_plot(self, y_true, y_pred, baseline_period, projection_period,
                                 model_name, adj_r2, data, input_col, output_col, model, site):
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
        # Ensure y_true and y_pred are pandas Series for indexing
        if not isinstance(y_true, pd.Series):
            y_true = pd.Series(y_true, name=output_col)
        if not isinstance(y_pred, pd.Series):
            y_pred = pd.Series(y_pred, name='Predicted')

        # Use the index from y_true as the x-axis
        x = y_true.index

        # Create figure
        fig, ax = plt.subplots(figsize=self.figsize)

        # Plot actual and predicted
        ax.plot(x, y_true, label='Actual', color='blue')
        ax.plot(x, y_pred, label='Predicted', color='orange', linestyle='--')

        # Shade baseline period
        if baseline_period:
            start_bl = pd.to_datetime(baseline_period[0])
            end_bl = pd.to_datetime(baseline_period[-1])
            ax.axvspan(start_bl, end_bl, color='green',
                       alpha=0.1, label='Baseline')

        # Shade projection period
        if projection_period:
            start_pr = pd.to_datetime(projection_period[0])
            end_pr = pd.to_datetime(projection_period[-1])
            ax.axvspan(start_pr, end_pr, color='red',
                       alpha=0.1, label='Projection')

        # Title and labels
        ax.set_title(f'{site} - {model_name} (Adj R² = {adj_r2:.3f})')
        ax.set_xlabel('Time')
        ax.set_ylabel(output_col)
        ax.legend()

        self.count += 1
        return fig
