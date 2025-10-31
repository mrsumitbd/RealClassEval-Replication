
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

        # Prepare data for plotting
        df = data.copy()
        df = df.reset_index(drop=True)
        df['y_true'] = y_true.values if isinstance(
            y_true, pd.Series) else y_true
        df['y_pred'] = y_pred

        # Create a period column for coloring
        df['Period'] = 'Other'
        df.loc[df.index.isin(baseline_period), 'Period'] = 'Baseline'
        df.loc[df.index.isin(projection_period), 'Period'] = 'Projection'

        # If baseline_period and projection_period are lists of strings (e.g., years), map accordingly
        if isinstance(baseline_period[0], str) or isinstance(projection_period[0], str):
            if 'Year' in df.columns:
                df['Period'] = 'Other'
                df.loc[df['Year'].isin(baseline_period), 'Period'] = 'Baseline'
                df.loc[df['Year'].isin(projection_period),
                       'Period'] = 'Projection'
            elif 'Date' in df.columns:
                df['Period'] = 'Other'
                df.loc[df['Date'].astype(str).isin(
                    baseline_period), 'Period'] = 'Baseline'
                df.loc[df['Date'].astype(str).isin(
                    projection_period), 'Period'] = 'Projection'

        # Plot
        fig, ax = plt.subplots(figsize=self.figsize)
        # Plot actual values
        ax.plot(df.index, df['y_true'], label='Actual',
                color='black', linewidth=2)
        # Plot predicted values
        ax.plot(df.index, df['y_pred'], label='Predicted',
                color='red', linestyle='--', linewidth=2)

        # Highlight baseline and projection periods
        if 'Year' in df.columns:
            x_baseline = df[df['Period'] == 'Baseline'].index
            x_projection = df[df['Period'] == 'Projection'].index
        else:
            x_baseline = df[df['Period'] == 'Baseline'].index
            x_projection = df[df['Period'] == 'Projection'].index

        if len(x_baseline) > 0:
            ax.axvspan(x_baseline.min(), x_baseline.max(),
                       color='green', alpha=0.1, label='Baseline')
        if len(x_projection) > 0:
            ax.axvspan(x_projection.min(), x_projection.max(),
                       color='blue', alpha=0.1, label='Projection')

        # Title and labels
        title = f"{site} - {model_name} (Adj R2: {adj_r2:.3f})"
        ax.set_title(title)
        ax.set_xlabel('Index')
        ax.set_ylabel(output_col)
        ax.legend()
        plt.tight_layout()
        plt.show()
        return fig
