
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

        # Plot the true values
        plt.plot(y_true.index, y_true, label='True Values', color='blue')

        # Plot the predicted values
        plt.plot(y_true.index, y_pred, label='Predicted Values', color='red')

        # Plot the baseline period
        plt.axvspan(y_true.index[0], y_true.index[baseline_period],
                    color='gray', alpha=0.3, label='Baseline Period')

        # Plot the projection period
        plt.axvspan(y_true.index[baseline_period], y_true.index[baseline_period +
                    projection_period], color='green', alpha=0.3, label='Projection Period')

        # Add title and labels
        plt.title(
            f'{model_name} - Baseline and Projection Periods\nAdjusted R2: {adj_r2:.2f}')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.legend()

        # Show the plot
        plt.show()
