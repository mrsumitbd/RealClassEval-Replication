
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


class Plot_Data:

    def __init__(self, figsize=(18, 5)):
        self.figsize = figsize

    def correlation_plot(self, data):
        plt.figure(figsize=self.figsize)
        sns.heatmap(data.corr(), annot=True, cmap='coolwarm', square=True)
        plt.title('Correlation Plot')
        plt.show()

    def baseline_projection_plot(self, y_true, y_pred, baseline_period, projection_period, model_name, adj_r2, data, input_col, output_col, model, site):
        plt.figure(figsize=self.figsize)
        plt.plot(y_true.index, y_true.values, label='Actual')
        plt.plot(y_pred.index, y_pred.values, label='Predicted')
        plt.axvline(x=baseline_period[1], color='r',
                    linestyle='--', label='Baseline Period End')
        plt.fill_between(baseline_period, y_true.min(),
                         y_true.max(), alpha=0.2, label='Baseline Period')
        plt.fill_between(projection_period, y_true.min(),
                         y_true.max(), alpha=0.2, label='Projection Period')
        plt.title(f'{site} - {model_name} (Adj. R2: {adj_r2:.2f})')
        plt.xlabel('Date')
        plt.ylabel(output_col)
        plt.legend()
        plt.show()

        # Additional plot to show feature importance if model is a tree-based model
        if hasattr(model, 'feature_importances_'):
            feature_importances = pd.DataFrame(
                {'Feature': input_col, 'Importance': model.feature_importances_})
            feature_importances = feature_importances.sort_values(
                by='Importance', ascending=False)
            plt.figure(figsize=(10, 6))
            sns.barplot(x='Feature', y='Importance', data=feature_importances)
            plt.title(f'{model_name} Feature Importances')
            plt.xlabel('Feature')
            plt.ylabel('Importance')
            plt.xticks(rotation=90)
            plt.show()
