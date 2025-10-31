import progressbar

class ProgressBar:
    """
    Progress bar for integration
    """

    def __init__(self, max_value=None):
        self.max_value = max_value
        if self.max_value is None:
            return
        self.counter = 0
        self.bar = progressbar.ProgressBar(max_value=self.max_value, widgets=[progressbar.ETA(), ' ', progressbar.Bar('#', '[', ']', '-'), progressbar.Percentage()])
        self.bar.start()

    def update(self):
        """Update progress bar"""
        try:
            self.counter += 1
            self.bar.update(self.counter)
        except AttributeError:
            pass

    def finish(self):
        """Finish progress bar"""
        try:
            self.bar.finish()
        except AttributeError:
            pass