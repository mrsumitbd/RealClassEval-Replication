import pandas as pd

class HeatStorage:

    def __init__(self):
        self.p = pd.DataFrame()
        self.e = pd.DataFrame()
        self.p_slack = pd.DataFrame()

    def _attributes(self):
        return ['p', 'e', 'p_slack']