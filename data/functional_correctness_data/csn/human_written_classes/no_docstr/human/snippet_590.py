import time

class FrameCounter:

    def __init__(self):
        self.render_times = []
        self.dt = 0.5

    def frame(self):
        self.render_times.append(time.time())

    def fps(self):
        now = time.time()
        while self.render_times and self.render_times[0] < now - self.dt:
            self.render_times.pop(0)
        return len(self.render_times) / max(self.dt, now - self.render_times[0] if self.render_times else self.dt)