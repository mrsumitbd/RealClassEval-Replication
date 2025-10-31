from collections import deque

class Tower:

    def __init__(self, disk_count=3, file=None):
        if disk_count < 1 or disk_count > 9:
            raise ValueError('disk_count must be between 1 and 9')
        self.disk_count = disk_count
        self.file = file
        self.disks = dict(left=deque(range(disk_count, 0, -1)), center=deque(), right=deque())
        self.started = False
        self.step = 0

    def draw(self) -> None:
        print('\n Step', self.step, file=self.file)
        print(file=self.file)
        for i in range(self.disk_count):
            n = self.disk_count - i - 1
            print(' ', end=' ', file=self.file)
            for pole in ['left', 'center', 'right']:
                if len(self.disks[pole]) - n > 0:
                    print(self.disks[pole][n], end=' ', file=self.file)
                else:
                    print(' ', end=' ', file=self.file)
            print(file=self.file)
        print('-' * 9, file=self.file)
        print(' ', 'L', 'C', 'R', file=self.file)

    def move(self, r) -> None:
        if not self.started:
            self.draw()
            self.started = True
        self.disks[str(r[1])].append(self.disks[str(r[0])].pop())
        self.step += 1
        self.draw()