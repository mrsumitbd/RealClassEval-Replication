from datetime import datetime

class _FlowStats:
    """
    An aggregator for flow records. Sums bytes and packets and keeps track of
    the active time window.
    """
    __slots__ = ['packets', 'bytes', 'start', 'end']

    def __init__(self):
        self.start = datetime.max
        self.end = datetime.min
        self.packets = 0
        self.bytes = 0

    def update(self, flow_record):
        if flow_record.start < self.start:
            self.start = flow_record.start
        if flow_record.end > self.end:
            self.end = flow_record.end
        self.packets += flow_record.packets
        self.bytes += flow_record.bytes

    def to_dict(self):
        return {x: getattr(self, x) for x in self.__slots__}