import numpy as np

class GAMWriter:
    """
    Writer object that converts a NormalFormgame into a game in
    GameTracer gam format.

    """

    @classmethod
    def to_file(cls, g, file_path):
        """
        Save the GameTracer gam format string representation of the
        NormalFormGame `g` to a file.

        Parameters
        ----------
        g : NormalFormGame

        file_path : str
            Path to the file to write to.

        """
        with open(file_path, 'w') as f:
            f.write(cls._dump(g) + '\n')

    @classmethod
    def to_string(cls, g):
        """
        Return a GameTracer gam format string representing the
        NormalFormGame `g`.

        Parameters
        ----------
        g : NormalFormGame

        Returns
        -------
        str
            String representation in gam format.

        """
        return cls._dump(g)

    @staticmethod
    def _dump(g):
        s = str(g.N) + '\n'
        s += ' '.join(map(str, g.nums_actions)) + '\n\n'
        for i, player in enumerate(g.players):
            payoffs = np.array2string(player.payoff_array.transpose((*range(g.N - i, g.N), *range(g.N - i))).ravel(order='F'))[1:-1]
            s += ' '.join(payoffs.split()) + ' '
        return s.rstrip()