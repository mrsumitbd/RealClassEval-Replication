from ncclient.xml_ import to_ele

class Notification:

    def __init__(self, raw):
        self._raw = raw
        self._root_ele = to_ele(raw)

    @property
    def notification_ele(self):
        return self._root_ele

    @property
    def notification_xml(self):
        return self._raw