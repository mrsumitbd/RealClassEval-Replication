class ProgressMonitor:

    def __init__(self, count):
        self.count, self.progress = (count, 0)

    def show(self, n=1):
        self.progress += n
        text = 'Completed {}/{} tasks'.format(self.progress, self.count)
        write_and_flush('\x08' * 80, '\r', text)

    def done(self):
        write_and_flush('\n')