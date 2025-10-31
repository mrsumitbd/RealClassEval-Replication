from neuromllite.utils import load_simulation_json
from neuromllite.utils import print_v
import os

class NeuroMLliteRunner:

    def __init__(self, nmllite_sim, simulator='jNeuroML'):
        real_sim = os.path.realpath(nmllite_sim)
        print_v('Created NeuroMLliteRunner to run %s in %s' % (real_sim, simulator))
        self.base_dir = os.path.dirname(real_sim)
        self.nmllite_sim = nmllite_sim
        self.simulator = simulator
    '\n        Run a single instance of the simulation, changing the parameters specified\n    '

    def run_once(self, job_dir, **kwargs):
        from neuromllite.utils import print_v
        from neuromllite.utils import load_simulation_json, load_network_json
        from neuromllite.NetworkGenerator import generate_and_run
        from pyneuroml.pynml import get_value_in_si
        print_v('Running NeuroMLlite simulation in dir: %s...' % job_dir)
        sim = load_simulation_json(self.nmllite_sim)
        import random
        sim.id = '%s%s' % (sim.id, '_%s' % kwargs['reference'] if 'reference' in kwargs else '')
        network = load_network_json(self.base_dir + '/' + sim.network)
        for a in kwargs:
            if a in network.parameters:
                print_v('  Setting %s to %s in network...' % (a, kwargs[a]))
                network.parameters[a] = kwargs[a]
            elif a in sim.allowed_fields:
                print_v('  Setting %s to %s in simulator...' % (a, kwargs[a]))
                setattr(sim, a, kwargs[a])
            else:
                print_v('  Cannot set parameter %s to %s in network or simulator...' % (a, kwargs[a]))
        traces, events = generate_and_run(sim, simulator=self.simulator, network=network, return_results=True, base_dir=self.base_dir, target_dir=job_dir)
        print_v('Returned traces: %s, events: %s' % (traces.keys(), events.keys()))
        return (traces, events)