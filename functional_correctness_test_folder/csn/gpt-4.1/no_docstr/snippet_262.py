
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import r2_score


class Plot_Data:

    def __init__(self, figsize=(18, 5)):
        self.figsize = figsize

    def correlation_plot(self, data):
        plt.figure(figsize=self.figsize)
        corr = data.corr()
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(corr, mask=mask, annot=True, fmt=".2f",
                    cmap='coolwarm', square=True, linewidths=.5)
        plt.title("Correlation Matrix")
        plt.tight_layout()
        plt.show()

    def baseline_projection_plot(self, y_true, y_pred, baseline_period, projection_period, model_name, adj_r2, data, input_col, output_col, model, site):
        plt.figure(figsize=self.figsize)
        plt.plot(data.index, y_true, label='Actual',
                 color='black', linewidth=2)
        plt.plot(data.index, y_pred, label='Predicted',
                 color='blue', linestyle='--', linewidth=2)
        plt.axvspan(baseline_period[0], baseline_period[1],
                    color='green', alpha=0.1, label='Baseline Period')
        plt.axvspan(projection_period[0], projection_period[1],
                    color='red', alpha=0.1, label='Projection Period')
        plt.xlabel('Date')
        plt.ylabel(output_col)
        plt.title(f"{model_name} Prediction at {site}\nAdj R2: {adj_r2:.3f}")
        plt.legend()
        plt.tight_layout()
        plt.show()
