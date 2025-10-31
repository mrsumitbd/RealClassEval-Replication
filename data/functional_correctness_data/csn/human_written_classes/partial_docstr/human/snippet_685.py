import numpy as np
from scipy.stats import gaussian_kde

class StrategynD:
    """
    A strategy that describes how to plot a model that depends on a multiple independent variables,
    and how to update that plot.
    """

    def __init__(self, interactive_guess):
        self.ig = interactive_guess

    def plot_data(self, proj, ax):
        """
        Creates and plots the contourplot of the original data. This is done
        by evaluating the density of projected datapoints on a grid.
        """
        x, y = proj
        x_data = self.ig.independent_data[x]
        y_data = self.ig.dependent_data[y]
        projected_data = np.column_stack((x_data, y_data)).T
        kde = gaussian_kde(projected_data)
        xx, yy = np.meshgrid(self.ig._x_points[x], self.ig._y_points[y])
        x_grid = xx.flatten()
        y_grid = yy.flatten()
        contour_grid = kde.pdf(np.column_stack((x_grid, y_grid)).T)
        if self.ig.log_contour:
            contour_grid = np.log(contour_grid)
            vmin = -7
        else:
            vmin = None
        ax.contourf(xx, yy, contour_grid.reshape(xx.shape), 50, vmin=vmin, cmap='Blues')

    def plot_model(self, proj, ax):
        """
        Plots the model proposed for the projection proj on ax.
        """
        x, y = proj
        evaluated_model = self.ig._eval_model()
        y_vals = getattr(evaluated_model, y.name)
        x_vals = self.ig._x_grid[x]
        plot = ax.errorbar(x_vals, y_vals, xerr=0, yerr=0, c='red')
        return plot

    def update_plot(self, indep_var, dep_var):
        """
        Updates the plot of the proposed model.
        """
        evaluated_model = self.ig._eval_model()
        y_vals = getattr(evaluated_model, dep_var.name)
        x_vals = self.ig._x_grid[indep_var]
        x_plot_data = []
        y_plot_data = []
        y_plot_error = []
        for x_val in self.ig._x_points[indep_var]:
            idx_mask = x_vals == x_val
            xs = x_vals[idx_mask]
            x_plot_data.append(xs[0])
            ys = y_vals[idx_mask]
            y_plot_data.append(np.mean(ys))
            y_error = np.percentile(ys, self.ig.percentile)
            y_plot_error.append(y_error)
        x_plot_data = np.array(x_plot_data)
        y_plot_data = np.array(y_plot_data)
        y_plot_error = np.array(y_plot_error)
        xs = np.column_stack((x_plot_data, x_plot_data))
        yerr = y_plot_error + y_plot_data[:, np.newaxis]
        y_segments = np.dstack((xs, yerr))
        plot_line, caps, error_lines = self.ig._plots[indep_var, dep_var]
        plot_line.set_data(x_plot_data, y_plot_data)
        error_lines[1].set_segments(y_segments)