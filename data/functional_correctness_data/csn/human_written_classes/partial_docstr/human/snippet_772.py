from collections.abc import Iterable

class CliVariants:
    """
    Provides an interface for cli variants (typically to handle a transition
    period for a deprecated cli)

    Instance must be initialized either with 2 or more str variants:
        ``CliVariants( 'new cli', 'legacy cli' )``,
    or with 2 or more sequences of cli (or a mix of list and str types), e.g.:
        ``CliVariants( ['new cli1', 'new cli2'], 'alt cli3', 'legacy cli4' )``
    """

    @staticmethod
    def expand(cmds):
        """ Expands cmds argument into a list of all CLI variants

        The method returns a list of all full variant combinations present
        in the the cmds arguement

        Args:
            cmds (list): a list made of str and CliVariants types

        Returns:
            expanded list, e.g.:
                expand( 'x', CliVariants( 'a', 'b'), 'y' )
                will return: [ ['x', 'a', 'y'], ['x', 'b', 'y'] ]
        """
        assert isinstance(cmds, list), 'argument cmds must be list type'
        if not cmds:
            return [[]]
        head = cmds[0]
        tail = cmds[1:]
        if isinstance(head, CliVariants):
            return [v + e for v in head.variants for e in CliVariants.expand(tail)]
        else:
            return [[head] + e for e in CliVariants.expand(tail)]

    def __init__(self, *cli):
        assert len(cli) >= 2, 'must be initialized with 2 or more arguments'
        self.variants = [v if not isinstance(v, str) and isinstance(v, Iterable) else [v] for v in cli]