
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D


class Plot_Data:

    def __init__(self, figsize=(18, 5)):
        self.figsize = figsize

    def correlation_plot(self, data):
        plt.figure(figsize=self.figsize)
        corr = data.corr()
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(corr, mask=mask, annot=True, cmap='coolwarm', center=0)
        plt.title('Correlation Matrix')
        plt.show()

    def baseline_projection_plot(self, y_true, y_pred, baseline_period, projection_period, model_name, adj_r2, data, input_col, output_col, model, site):
        plt.figure(figsize=self.figsize)

        # Plot true values
        plt.plot(data.index, y_true, label='True Values',
                 color='blue', alpha=0.7)

        # Plot predicted values
        plt.plot(data.index, y_pred, label='Predicted Values',
                 color='red', linestyle='--', alpha=0.7)

        # Add vertical line to separate baseline and projection periods
        plt.axvline(x=baseline_period[-1],
                    color='black', linestyle=':', linewidth=2)

        # Add text for baseline and projection periods
        plt.text(baseline_period[0], plt.ylim()[
                 1] * 0.9, 'Baseline Period', fontsize=10, bbox=dict(facecolor='white', alpha=0.5))
        plt.text(projection_period[0], plt.ylim()[
                 1] * 0.9, 'Projection Period', fontsize=10, bbox=dict(facecolor='white', alpha=0.5))

        # Add model and site info
        plt.title(f'{model_name} - {site}\nAdjusted R²: {adj_r2:.2f}')
        plt.xlabel('Date')
        plt.ylabel(output_col)

        # Add legend
        plt.legend()

        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()
