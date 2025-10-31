import xbos_services_getter as xsg
from DataManager.DataManager import DataManager
from Optimizers.MPC.MPC import Node
import datetime
import datetime
from Optimizers.MPC.MPC import MPC

class SimulationMPC:

    def __init__(self, building, zones, lambda_val, start, end, forecasting_horizon, window, tstats, non_contrallable_data=None):
        """

        :param building:
        :param zones:
        :param lambda_val:
        :param start: datetime with timezone
        :param end: datetime with timezone
        :param forecasting_horizon:
        :param window:
        :param tstats:
        :param non_contrallable_data:
        """
        assert xsg.get_window_in_sec(forecasting_horizon) % xsg.get_window_in_sec(window) == 0
        self.building = building
        self.zones = zones
        self.window = window
        self.lambda_val = lambda_val
        self.forecasting_horizon = forecasting_horizon
        self.delta_forecasting_horizon = datetime.timedelta(seconds=xsg.get_window_in_sec(forecasting_horizon))
        self.delta_window = datetime.timedelta(seconds=xsg.get_window_in_sec(window))
        self.simulation_end = end
        end += self.delta_forecasting_horizon
        self.DataManager = DataManager(building, zones, start, end, window, non_contrallable_data)
        self.tstats = tstats
        self.current_time = start
        self.current_time_step = 0
        self.actions = {iter_zone: [] for iter_zone in self.zones}
        self.temperatures = {iter_zone: [self.tstats[iter_zone].temperature] for iter_zone in self.zones}

    def step(self):
        start_mpc = self.current_time
        end_mpc = self.current_time + self.delta_forecasting_horizon
        non_controllable_data = {'comfortband': {iter_zone: self.DataManager.comfortband[iter_zone].loc[start_mpc:end_mpc] for iter_zone in self.zones}, 'do_not_exceed': {iter_zone: self.DataManager.do_not_exceed[iter_zone].loc[start_mpc:end_mpc] for iter_zone in self.zones}, 'occupancy': {iter_zone: self.DataManager.occupancy[iter_zone].loc[start_mpc:end_mpc] for iter_zone in self.zones}, 'outdoor_temperature': self.DataManager.outdoor_temperature.loc[start_mpc:end_mpc]}
        op = MPC(self.building, self.zones, start_mpc, end_mpc, self.window, self.lambda_val, non_controllable_data=non_controllable_data, debug=False)
        root = Node({iter_zone: self.tstats[iter_zone].temperature for iter_zone in self.zones}, 0)
        root = op.shortest_path(root)
        best_action = op.g.node[root]['best_action']
        self.current_time += self.delta_window
        self.current_time_step += 1
        for iter_zone in self.zones:
            self.temperatures[iter_zone].append(self.tstats[iter_zone].next_temperature(best_action[iter_zone]))
            self.actions[iter_zone].append(best_action[iter_zone])
        return root

    def run(self):
        while self.current_time < self.simulation_end:
            self.step()