
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
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax,
                    cbar_kws={'label': 'Pearson r'})
        ax.set_title('Correlation Heatmap', fontsize=16)
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
        # Ensure y_true is a Series with a datetime index or a column named 'date'
        if isinstance(y_true, pd.Series):
            y_true = y_true.copy()
        else:
            raise ValueError("y_true must be a pandas Series")

        # Convert y_pred to a Series aligned with y_true
        y_pred_series = pd.Series(y_pred, index=y_true.index, name='Predicted')

        # Create figure with two subplots: baseline and projection
        fig, axes = plt.subplots(1, 2, figsize=self.figsize, sharey=True)
        fig.suptitle(
            f'{site} - {model_name} (Adj R² = {adj_r2:.3f})', fontsize=18)

        # Baseline plot
        ax_base = axes[0]
        base_mask = y_true.index.isin(baseline_period)
        ax_base.plot(y_true.index[base_mask],
                     y_true[base_mask], label='Actual', color='black')
        ax_base.plot(y_pred_series.index[base_mask], y_pred_series[base_mask], label='Predicted',
                     color='red', linestyle='--')
        ax_base.set_title('Baseline Period')
        ax_base.set_xlabel('Date')
        ax_base.set_ylabel(output_col)
        ax_base.legend()
        ax_base.grid(True)

        # Projection plot
        ax_proj = axes[1]
        proj_mask = y_true.index.isin(projection_period)
        ax_proj.plot(y_true.index[proj_mask],
                     y_true[proj_mask], label='Actual', color='black')
        ax_proj.plot(y_pred_series.index[proj_mask], y_pred_series[proj_mask], label='Predicted',
                     color='red', linestyle='--')
        ax_proj.set_title('Projection Period')
        ax_proj.set_xlabel('Date')
        ax_proj.legend()
        ax_proj.grid(True)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        self.count += 1
        return fig
