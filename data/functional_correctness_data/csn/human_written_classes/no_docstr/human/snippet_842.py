import pandas as pd

class LineVariables:

    def __init__(self):
        self.p = pd.DataFrame()
        self.q = pd.DataFrame()
        self.ccm = pd.DataFrame()

    def _attributes(self):
        return ['p', 'q', 'ccm']