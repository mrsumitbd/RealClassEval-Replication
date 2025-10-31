import sys

class ProgressBar:

    def __init__(self):
        self.last_update = 0
        self.update_every = 2 * 1024 * 1024
        sys.stdout.write('0%')
        sys.stdout.flush()

    def update(self, monitor):
        self.update_every = min(self.update_every, monitor.len / 30)
        if monitor.bytes_read - self.last_update >= self.update_every:
            sys.stdout.write('.')
            old_percent = float(self.last_update) / monitor.len
            new_percent = float(monitor.bytes_read) / monitor.len
            for step in range(90, 0, -10):
                step /= 100.0
                if new_percent >= step > old_percent:
                    sys.stdout.write('{:.0%}'.format(step))
                    break
            sys.stdout.flush()
            self.last_update = monitor.bytes_read