
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
        plt.title('Correlation Matrix')
        plt.show()

    def baseline_projection_plot(self, y_true, y_pred, baseline_period, projection_period, model_name, adj_r2, data, input_col, output_col, model, site):
        plt.figure(figsize=self.figsize)
        plt.plot(y_true.index, y_true, label='Actual')
        plt.plot(y_pred.index, y_pred, label=f'{model_name} Prediction')
        plt.axvline(x=baseline_period[1], color='r',
                    linestyle='--', label='Baseline Period End')
        plt.fill_between(baseline_period, y_true.min(),
                         y_true.max(), alpha=0.2, label='Baseline Period')
        plt.fill_between(projection_period, y_true.min(),
                         y_true.max(), alpha=0.2, label='Projection Period')
        plt.title(f'{site} {output_col} - {model_name} (Adj. R2: {adj_r2:.2f})')
        plt.xlabel('Date')
        plt.ylabel(output_col)
        plt.legend()
        plt.show()

        # Print model coefficients if available
        if hasattr(model, 'coef_'):
            print(f'{model_name} Coefficients:')
            for feature, coef in zip(input_col, model.coef_):
                print(f'{feature}: {coef:.2f}')
        elif hasattr(model, 'feature_importances_'):
            print(f'{model_name} Feature Importances:')
            for feature, importance in zip(input_col, model.feature_importances_):
                print(f'{feature}: {importance:.2f}')
