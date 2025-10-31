class Strategy2D:
    """
    A strategy that describes how to plot a model that depends on a single independent variable,
    and how to update that plot.
    """

    def __init__(self, interactive_guess):
        self.ig = interactive_guess

    def plot_data(self, proj, ax):
        """
        Creates and plots a scatter plot of the original data.
        """
        x, y = proj
        ax.scatter(self.ig.independent_data[x], self.ig.dependent_data[y], c='b')

    def plot_model(self, proj, ax):
        """
        Plots the model proposed for the projection proj on ax.
        """
        x, y = proj
        y_vals = getattr(self.ig._eval_model(), y.name)
        x_vals = self.ig._x_points[x]
        plot, = ax.plot(x_vals, y_vals, c='red')
        return plot

    def update_plot(self, indep_var, dep_var):
        """
        Updates the plot of the proposed model.
        """
        evaluated_model = self.ig._eval_model()
        plot = self.ig._plots[indep_var, dep_var]
        y_vals = getattr(evaluated_model, dep_var.name)
        x_vals = self.ig._x_points[indep_var]
        plot.set_data(x_vals, y_vals)