class Finder:

    def __init__(self, file, segments):
        self.file = file
        self.segments = segments
        self.make_index()

    def make_index(self):
        self.values = []
        self.positions = []
        file.seek(0, 2)
        end = file.tell()
        step = end / (self.segments - 1)
        for i in range(0, self.segments - 1):
            file.seek(i * step, 0)
            file.readline()
            position = file.tell()
            fields = file.readline().split()
            self.values.append(int(fields[0]))
            self.positions.append(position)

    def scores_in_range(self, start, end):
        position = self.positions[-1]
        for i in range(1, len(self.values)):
            if self.values[i] > start:
                position = self.positions[i - 1]
                break
        self.file.seek(position, 0)
        result = []
        while True:
            line = file.readline()
            if line == '':
                break
            fields = line.split()
            pos = int(fields[0])
            if pos < start:
                continue
            if pos > end:
                break
            result.append((pos, fields[1]))
        return result