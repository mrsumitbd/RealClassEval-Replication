import collections

class ProgressBarSimulatorWrapper:
    """A wrapper class to show a progress bar for running a simulation
    """

    def __init__(self, sim, timeout=10, flush=False, **kwargs):
        """Constructor.

        Parameters
        ----------
        sim : Simulator
            A wrapped Simulator object
        timeout : float, optional
            An interval to update the progress bar. Given as seconds.
            Default is 10.
        flush : bool, optional
            Clear the output at finishing a simulation.
            Default is False.

        See Also
        --------
        ProgressBar

        """
        if int(timeout) <= 0:
            raise ValueError('timeout [{}] must be larger than 0.'.format(timeout))
        self.__sim = sim
        self.__timeout = timeout
        self.__flush = flush
        self.__kwargs = kwargs

    def run(self, duration, obs):
        """Run the simulation.

        Parameters
        ----------
        duration : Real
            a duration for running a simulation.
                A simulation is expected to be stopped at t() + duration.
        observers : list of Obeservers, optional
            observers

        """
        from ecell4_base.core import TimeoutObserver
        timeout = TimeoutObserver(self.__timeout)
        if isinstance(obs, collections.Iterable):
            obs = tuple(obs) + (timeout,)
        else:
            obs = (obs, timeout)
        p = ProgressBar(**self.__kwargs)
        p.animate(0.0)
        tstart = self.__sim.t()
        upto = tstart + duration
        while self.__sim.t() < upto:
            self.__sim.run(upto - self.__sim.t(), obs)
            p.animate((self.__sim.t() - tstart) / duration, timeout.accumulation())
        if self.__flush:
            p.flush()
        else:
            print()

    def __getattr__(self, key):
        return getattr(self.__sim, key)