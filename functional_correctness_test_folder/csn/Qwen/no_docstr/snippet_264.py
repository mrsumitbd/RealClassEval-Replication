
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


class Plot_Data:

    def __init__(self, figsize=(18, 5)):
        self.figsize = figsize

    def correlation_plot(self, data):
        plt.figure(figsize=self.figsize)
        correlation_matrix = data.corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlation Matrix')
        plt.show()

    def baseline_projection_plot(self, y_true, y_pred, baseline_period, projection_period, model_name, adj_r2, data, input_col, output_col, model, site):
        plt.figure(figsize=self.figsize)

        # Plotting baseline period
        plt.plot(data[input_col].loc[baseline_period],
                 data[output_col].loc[baseline_period], label='Actual (Baseline)', color='blue')

        # Plotting projection period
        plt.plot(data[input_col].loc[projection_period], y_true,
                 label='Actual (Projection)', color='green')
        plt.plot(data[input_col].loc[projection_period], y_pred,
                 label=f'Predicted ({model_name})', color='red', linestyle='--')

        plt.title(f'Baseline and Projection Plot for {site}')
        plt.xlabel(input_col)
        plt.ylabel(output_col)
        plt.legend()
        plt.text(0.05, 0.95, f'Adj R^2: {adj_r2:.2f}', transform=plt.gca(
        ).transAxes, fontsize=12, verticalalignment='top')
        plt.grid(True)
        plt.show()
