from neuron import h

class IzhiCell:
    """Create an izhikevich cell based on 2007 parameterization using either izhi2007.mod (no hosting section) or izhi2007b.mod (v in created section)
    If host is omitted or None, this will be a section-based version that uses Izhi2007b with state vars v, u where v is the section voltage
    If host is given then this will be a shared unused section that simply houses an Izhi2007 using state vars V and u
    Note: Capacitance 'C' differs from sec.cm which will be 1; vr is RMP; vt is threshold; vpeak is peak voltage
  """

    def __init__(self, type='tonic spiking', host=None, cellid=-1):
        self.type = type
        if host is None:
            self.sec = h.Section(name='izhi2003' + type + str(cellid))
            self.sec.L, self.sec.diam = (6.3, 5)
            self.izh = h.Izhi2003b(0.5, sec=self.sec)
        else:
            self.sec = dummy
            self.izh = h.Izhi2003a(0.5, sec=self.sec)
        self.izh.a, self.izh.b, self.izh.c, self.izh.d = type2003[type]
        self.izh.Iin = 0

    def init(self):
        self.sec(0.5).v = self.vinit

    def reparam(self, type='tonic spiking', cellid=-1):
        self.type = type
        self.izh.a, self.izh.b, self.izh.c, self.izh.d = type2003[type]