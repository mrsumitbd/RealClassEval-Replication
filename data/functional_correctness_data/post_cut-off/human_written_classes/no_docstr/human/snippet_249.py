class ClusterStatus:

    def __init__(self):
        self.finished = False

    def finish(self) -> None:
        self.finished = True

    def running(self) -> bool:
        return not self.finished