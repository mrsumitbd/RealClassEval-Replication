import time as sys_time

class vrep_time:

    def __init__(self, vrep_io):
        self.io = vrep_io

    def get_time(self, trial=0):
        t = self.io.get_simulation_current_time()
        if t == 0:
            sys_time.sleep(0.5)
            return self.get_time(trial + 1)
        if trial > 10:
            raise EnvironmentError('Could not get current simulation time. Make sure the V-REP simulation is running. And that you have added the "time" child script to your scene.')
        return t

    def sleep(self, t):
        if t > 1000:
            logger.warning('Big vrep sleep: {}'.format(t))
            t = 1
        t0 = self.get_time()
        while self.get_time() - t0 < t:
            if self.get_time() < t0:
                break
            sys_time.sleep(0.01)