
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import r2_score


class Plot_Data:

    def __init__(self, figsize=(18, 5)):

        self.figsize = figsize

    def correlation_plot(self, data):

        plt.figure(figsize=self.figsize)
        sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
        plt.title('Correlation Plot')
        plt.show()

    def baseline_projection_plot(self, y_true, y_pred, baseline_period, projection_period, model_name, adj_r2, data, input_col, output_col, model, site):

        plt.figure(figsize=self.figsize)

        # Plot the actual data
        plt.plot(data[input_col], data[output_col],
                 label='Actual Data', color='blue')

        # Plot the baseline period
        plt.axvspan(baseline_period[0], baseline_period[1],
                    color='gray', alpha=0.3, label='Baseline Period')

        # Plot the projection period
        plt.axvspan(projection_period[0], projection_period[1],
                    color='green', alpha=0.3, label='Projection Period')

        # Plot the predicted data
        plt.plot(data[input_col], y_pred, label='Predicted Data',
                 color='red', linestyle='--')

        # Add title and labels
        plt.title(
            f'{model_name} - Baseline and Projection Periods\nAdjusted R2: {adj_r2:.2f}')
        plt.xlabel(input_col)
        plt.ylabel(output_col)
        plt.legend()

        plt.show()
