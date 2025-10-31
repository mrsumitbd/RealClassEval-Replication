import threading

class CostManager:

    def __init__(self):
        self.total_input_tokens = {}
        self.total_output_tokens = {}
        self.total_tokens = {}
        self.total_input_cost = {}
        self.total_output_cost = {}
        self.total_cost = {}
        self._lock = threading.Lock()

    def get_total_cost(self):
        total_cost = 0.0
        for model in self.total_cost.keys():
            total_cost += self.total_cost[model]
        return total_cost