import sys

class Device:
    """
    A device.
    """

    @staticmethod
    def factory(_str):
        """
        Device factory.
        :param _str:
        :type _str:
        :return:
        :rtype:
        """
        _str = _str.decode('utf-8')
        if DEBUG:
            print('Device.factory(', _str, ')', file=sys.stderr)
            print('   _str=', repr(_str), file=sys.stderr)
            print('   _str=', _str.replace(' ', '_'), file=sys.stderr)
        values = _str.split(None, 2)
        if DEBUG:
            print('values=', values, file=sys.stderr)
        return Device(*values)

    def __init__(self, serialno, status, qualifiers=None):
        """
        Constructor.
        :param serialno:
        :type serialno:
        :param status:
        :type status:
        :param qualifiers:
        :type qualifiers:
        """
        self.serialno = serialno
        self.status = status
        self.qualifiers = qualifiers.split(None) if qualifiers else None

    def has_qualifier(self, qualifier):
        """

        :param qualifier:
        :type qualifier:
        :return:
        :rtype:
        """
        return self.qualifiers and qualifier in self.qualifiers

    def __str__(self):
        return '<<<' + self.serialno + ', ' + self.status + ', %s>>>' % self.qualifiers