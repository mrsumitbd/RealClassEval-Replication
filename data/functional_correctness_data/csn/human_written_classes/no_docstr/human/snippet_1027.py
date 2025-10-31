class DetailOptionParser:

    def __init__(self, detail_option):
        self._option_detail = detail_option
        self._excute = None

    def add_argument(self, option, excute):
        if self._option_detail == option:
            self._excute = excute

    def parse(self):
        self._excute.excute()