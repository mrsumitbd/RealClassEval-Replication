class ModbusDataBank:
    """
    Preliminary DataBank implementation for Modbus.

    This is a very generic implementation of a databank for Modbus. It's meant to set the
    groundwork for future implementations. Only derived classes should be instantiated, not
    this class directly. The signature of this __init__ method is subject to change.

    :param kwargs: Configuration
    """

    def __init__(self, **kwargs) -> None:
        self._data = kwargs['data']
        self._start_addr = kwargs['start_addr']

    def get(self, addr, count):
        """
        Read list of ``count`` values at ``addr`` memory location in DataBank.

        :param addr: Address to read from
        :param count: Number of entries to retrieve
        :return: list of entry values
        :except IndexError: Raised if address range falls outside valid range
        """
        addr -= self._start_addr
        data = self._data[addr:addr + count]
        if len(data) != count:
            addr += self._start_addr
            raise IndexError('Invalid address range [{:#06x} - {:#06x}]'.format(addr, addr + count))
        return data

    def set(self, addr, values) -> None:
        """
        Write list ``values`` to ``addr`` memory location in DataBank.

        :param addr: Address to write to
        :param values: list of values to write
        :except IndexError: Raised if address range falls outside valid range
        """
        addr -= self._start_addr
        end = addr + len(values)
        if not 0 <= addr <= end <= len(self._data):
            addr += self._start_addr
            raise IndexError('Invalid address range [{:#06x} - {:#06x}]'.format(addr, addr + len(values)))
        self._data[addr:end] = values