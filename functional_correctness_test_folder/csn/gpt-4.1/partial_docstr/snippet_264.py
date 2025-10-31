
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
        self.figsize = figsize
        self.count = 0

    def correlation_plot(self, data):
        '''
        Plots a correlation heatmap for the given DataFrame.
        Parameters
        ----------
        data : pd.DataFrame
            Data for which to plot the correlation matrix.
        '''
        self.count += 1
        plt.figure(figsize=self.figsize)
        corr = data.corr()
        sns.heatmap(corr, annot=True, fmt=".2f",
                    cmap='coolwarm', square=True, cbar=True)
        plt.title('Correlation Matrix')
        plt.tight_layout()
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

        # Prepare time axis
        if 'date' in data.columns:
            time = pd.to_datetime(data['date'])
        elif 'time' in data.columns:
            time = pd.to_datetime(data['time'])
        else:
            time = data.index

        # Prepare baseline and projection masks
        baseline_mask = data['date'].isin(
            baseline_period) if 'date' in data.columns else [False]*len(data)
        projection_mask = data['date'].isin(
            projection_period) if 'date' in data.columns else [False]*len(data)

        # Plot
        fig, ax = plt.subplots(figsize=self.figsize)
        # Plot actual values
        ax.plot(time, y_true, label='Actual', color='black', linewidth=2)
        # Plot predicted values
        ax.plot(time, y_pred, label='Predicted',
                color='red', linestyle='--', linewidth=2)
        # Highlight baseline period
        if any(baseline_mask):
            ax.axvspan(time[baseline_mask].min(), time[baseline_mask].max(
            ), color='green', alpha=0.1, label='Baseline Period')
        # Highlight projection period
        if any(projection_mask):
            ax.axvspan(time[projection_mask].min(), time[projection_mask].max(
            ), color='blue', alpha=0.1, label='Projection Period')

        ax.set_xlabel('Time')
        ax.set_ylabel(output_col)
        title = f"{site} - {model_name} (Adj R2: {adj_r2:.3f})"
        ax.set_title(title)
        ax.legend()
        plt.tight_layout()
        plt.show()
        return fig
