class RepeatedGame:
    """
    Class representing an N-player repeated game.

    Parameters
    ----------
    stage_game : NormalFormGame
        The stage game used to create the repeated game.

    delta : scalar(float)
        The common discount rate at which all players discount the future.

    Attributes
    ----------
    sg : NormalFormGame
        The stage game. See Parameters.

    delta : scalar(float)
        See Parameters.

    N : scalar(int)
        The number of players.

    nums_actions : tuple(int)
        Tuple of the numbers of actions, one for each player.
    """

    def __init__(self, stage_game, delta):
        self.sg = stage_game
        self.delta = delta
        self.N = stage_game.N
        self.nums_actions = stage_game.nums_actions

    def equilibrium_payoffs(self, method=None, options=None):
        """
        Compute the set of payoff pairs of all pure-strategy subgame-perfect
        equilibria with public randomization for any repeated two-player games
        with perfect monitoring and discounting.

        Parameters
        ----------
        method : str, optional
            The method for solving the equilibrium payoff set.

        options : dict, optional
            A dictionary of method options. For example, 'abreu_sannikov'
            method accepts the following options:

                tol : scalar(float)
                    Tolerance for convergence checking.
                max_iter : scalar(int)
                    Maximum number of iterations.
                u_init : ndarray(float, ndim=1)
                    The initial guess of threat points.

        Returns
        -------
        ndarray(float, ndim=2)
            Array containing the set of equilibrium payoff pairs.

        Notes
        -----
        Here lists all the implemented methods. The default method
        is 'abreu_sannikov'.

            1. 'abreu_sannikov'
        """
        if method is None:
            method = 'abreu_sannikov'
        if options is None:
            options = {}
        if method in ('abreu_sannikov', 'AS'):
            return _equilibrium_payoffs_abreu_sannikov(self, **options)
        else:
            msg = f'method {method} not supported.'
            raise NotImplementedError(msg)