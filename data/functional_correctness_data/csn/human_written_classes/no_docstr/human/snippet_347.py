class Packet:

    def __init__(self, l, i, k):
        self.link = l
        self.ident = i
        self.kind = k
        self.datum = 0
        self.data = [0] * BUFSIZE

    def append_to(self, lst):
        self.link = None
        if lst is None:
            return self
        else:
            p = lst
            next = p.link
            while next is not None:
                p = next
                next = p.link
            p.link = self
            return lst