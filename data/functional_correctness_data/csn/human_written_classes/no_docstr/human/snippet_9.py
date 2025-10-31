class MetadataProgress:

    def __init__(self, progressbar_class, enable: bool=True):
        self.progressbar_class = progressbar_class
        self.progressbar = self.progressbar_class(total=100, desc='Linearizing', unit='%', disable=not enable)

    def __enter__(self):
        self.progressbar.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self.progressbar.__exit__(exc_type, exc_value, traceback)

    def __call__(self, percent: int):
        if not self.progressbar_class:
            return
        self.progressbar.update(completed=percent)