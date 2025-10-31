import pandas as pd

class GridSlacks:

    def __init__(self):
        self.gen_d_crt = pd.DataFrame()
        self.gen_nd_crt = pd.DataFrame()
        self.load_shedding = pd.DataFrame()
        self.cp_load_shedding = pd.DataFrame()
        self.hp_load_shedding = pd.DataFrame()
        self.hp_operation_slack = pd.DataFrame()

    def _attributes(self):
        return ['gen_d_crt', 'gen_nd_crt', 'load_shedding', 'cp_load_shedding', 'hp_load_shedding', 'hp_operation_slack']