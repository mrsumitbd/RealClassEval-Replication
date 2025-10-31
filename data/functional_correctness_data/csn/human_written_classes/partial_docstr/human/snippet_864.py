class PerformanceModel:
    """Base class for performance models"""
    name = 'performance-model name'

    @classmethod
    def configure_arggroup(cls, parser):
        """Configure argument parser."""
        pass

    def __init__(self):
        self.results = {}

    def analyze(self):
        """Analyze the kernel with regard to the machine definition and cli arguments passed."""
        raise NotImplementedError()

    def report(self):
        """Return a readable text output with analysis report."""
        raise NotImplementedError()