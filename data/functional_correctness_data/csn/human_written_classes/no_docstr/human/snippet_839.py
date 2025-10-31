import pandas as pd

class BatteryStorage:

    def __init__(self):
        self.p = pd.DataFrame()
        self.e = pd.DataFrame()

    def _attributes(self):
        return ['p', 'e']