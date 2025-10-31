from os import fspath

class PTHWheelPiggyback:

    def __init__(self, strategy):
        self.strategy = strategy

    def __enter__(self):
        self.strategy.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.strategy.__exit__(exc_type, exc_val, exc_tb)

    def __call__(self, wheel, files, mapping):
        self.strategy(wheel, files, mapping)
        wheel.writestr(fspath(pth_file.name), pth_file.read_bytes())