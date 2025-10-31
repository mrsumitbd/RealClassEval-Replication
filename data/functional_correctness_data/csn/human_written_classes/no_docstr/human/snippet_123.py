from hijridate import Gregorian, Hijri

class hijri:

    @classmethod
    def to_gregorian(cls, year=None, month=None, day=None):
        g = Hijri(year=year, month=month, day=day, validate=False).to_gregorian()
        return g.datetuple()

    @classmethod
    def from_gregorian(cls, year=None, month=None, day=None):
        h = Gregorian(year, month, day).to_hijri()
        return h.datetuple()

    @classmethod
    def month_length(cls, year, month):
        h = Hijri(year=year, month=month, day=1)
        return h.month_length()