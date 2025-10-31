
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


class Plot_Data:

    def __init__(self, figsize=(18, 5)):
        self.figsize = figsize

    def correlation_plot(self, data):
        plt.figure(figsize=self.figsize)
        sns.heatmap(data.corr(), annot=True, cmap='coolwarm', center=0)
        plt.title('Correlation Matrix')
        plt.show()

    def baseline_projection_plot(self, y_true, y_pred, baseline_period, projection_period, model_name, adj_r2, data, input_col, output_col, model, site):
        plt.figure(figsize=self.figsize)

        # Plot baseline data
        plt.plot(baseline_period, y_true, label='Actual', color='blue')
        plt.plot(baseline_period, y_pred, label='Predicted',
                 color='red', linestyle='--')

        # Plot projection data
        plt.plot(projection_period, model.predict(data[input_col].loc[projection_period]),
                 label='Projection', color='green', linestyle='-.')

        plt.title(f'{model_name} - {site}\nAdj R2: {adj_r2:.2f}')
        plt.xlabel('Date')
        plt.ylabel(output_col)
        plt.legend()
        plt.grid(True)
        plt.show()
