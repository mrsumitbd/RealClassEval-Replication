class Callback:

    def optimization_about_to_start(self):
        """This is called at the beginning of the optimization procedure."""

    def __call__(self, iteration, error, embedding):
        """This is the main method called from the optimization.

        Parameters
        ----------
        iteration: int
            The current iteration number.

        error: float
            The current KL divergence of the given embedding.

        embedding: TSNEEmbedding
            The current t-SNE embedding.

        Returns
        -------
        stop_optimization: bool
            If this value is set to ``True``, the optimization will be
            interrupted.

        """