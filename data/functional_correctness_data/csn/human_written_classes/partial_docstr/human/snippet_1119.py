class bulbs:
    """A simple class with a register and unregister methods"""

    def __init__(self):
        self.bulbs = []
        self.boi = None

    def register(self, bulb):
        global opts
        bulb.get_label()
        bulb.get_location()
        bulb.get_version()
        bulb.get_group()
        bulb.get_wififirmware()
        bulb.get_hostfirmware()
        self.bulbs.append(bulb)
        self.bulbs.sort(key=lambda x: x.label or x.mac_addr)
        if opts['extra']:
            bulb.register_callback(lambda y: print('Unexpected message: %s' % str(y)))

    def unregister(self, bulb):
        idx = 0
        for x in list([y.mac_addr for y in self.bulbs]):
            if x == bulb.mac_addr:
                del self.bulbs[idx]
                break
            idx += 1