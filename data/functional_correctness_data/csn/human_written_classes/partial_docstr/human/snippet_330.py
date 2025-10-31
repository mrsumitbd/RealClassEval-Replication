class _GetchMacCarbon:
    """
    A function which returns the current ASCII key that is down;
    if no ASCII key is down, the null string is returned.  The
    page http://www.mactech.com/macintosh-c/chap02-1.html was
    very helpful in figuring out how to do this.
    """

    def __init__(self):
        import Carbon
        Carbon.Evt

    def __call__(self):
        import Carbon
        if Carbon.Evt.EventAvail(8)[0] == 0:
            return ''
        else:
            what, msg, when, where, mod = Carbon.Evt.GetNextEvent(8)[1]
            return chr(msg & 255)