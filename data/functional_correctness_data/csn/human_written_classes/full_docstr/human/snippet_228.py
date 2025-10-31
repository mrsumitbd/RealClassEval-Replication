import datetime
from ait.core import log
import math
import calendar

class PCapRolloverStream:
    """
    Wraps a PCapStream to rollover to a new filename, based on packet
    times, file size, or number of packets.
    """

    def __init__(self, format, nbytes=None, npackets=None, nseconds=None, dryrun=False):
        """Creates a new :class:`PCapRolloverStream` with the given
        thresholds.

        A :class:`PCapRolloverStream` behaves like a
        :class:`PCapStream`, except that writing a new packet will
        cause the current file to be closed and a new file to be
        opened when one or more of thresholds (``nbytes``,
        ``npackets``, ``nseconds``) is exceeded.

        The new filename is determined by passing the ``format``
        string through :func:`PCapPacketHeader.timestamp.strftime()`
        for the first packet in the file.

        When segmenting based on time (``nseconds``), for file naming
        and interval calculation purposes ONLY, the timestamp of the
        first packet in the file is rounded down to nearest even
        multiple of the number of seconds.  This yields nice round
        number timestamps for filenames.  For example:

          PCapRolloverStream(format="%Y%m%dT%H%M%S.pcap", nseconds=3600)

        If the first packet written to a file has a time of 2017-11-23
        19:28:58, the file will be named:

            20171123T190000.pcap

        And a new file will be started when a packet is written with a
        timestamp that exceeds 2017-11-23 19:59:59.

        :param format:    Output filename in ``strftime(3)`` format
        :param nbytes:    Rollover after writing nbytes
        :param npackets:  Rollover after writing npackets
        :param nseconds:  Rollover after nseconds have elapsed between
                          the first and last packet timestamp in the file.
        :param dryrun:    Simulate file writes and output log messages.
        """
        self._dryrun = dryrun
        self._filename = None
        self._format = format
        self._startTime = None
        self._stream = None
        self._threshold = PCapFileStats(nbytes, npackets, nseconds)
        self._total = PCapFileStats(0, 0, 0)

    @property
    def rollover(self):
        """Indicates whether or not its time to rollover to a new file."""
        rollover = False
        if not rollover and self._threshold.nbytes is not None:
            rollover = self._total.nbytes >= self._threshold.nbytes
        if not rollover and self._threshold.npackets is not None:
            rollover = self._total.npackets >= self._threshold.npackets
        if not rollover and self._threshold.nseconds is not None:
            nseconds = math.ceil(self._total.nseconds)
            rollover = nseconds >= self._threshold.nseconds
        return rollover

    def write(self, bytes, header=None):
        """Writes packet ``bytes`` and the optional pcap packet ``header``.

        If the pcap packet ``header`` is not specified, one will be
        generated based on the number of packet ``bytes`` and current
        time.
        """
        if header is None:
            header = PCapPacketHeader(orig_len=len(bytes))
        if self._stream is None:
            if self._threshold.nseconds is not None:
                nseconds = self._threshold.nseconds
                remainder = int(math.floor(header.ts % nseconds))
                delta = datetime.timedelta(seconds=remainder)
                timestamp = header.timestamp - delta
            else:
                timestamp = header.timestamp
            self._filename = timestamp.strftime(self._format)
            self._startTime = calendar.timegm(timestamp.replace(microsecond=0).timetuple())
            if self._dryrun:
                self._stream = True
                self._total.nbytes += len(PCapGlobalHeader().pack())
            else:
                self._stream = open(self._filename, 'w')
                self._total.nbytes += len(self._stream.header.pack())
        if not self._dryrun:
            self._stream.write(bytes, header)
        self._total.nbytes += len(bytes) + len(header)
        self._total.npackets += 1
        self._total.nseconds = header.ts - self._startTime
        if self.rollover:
            self.close()
        return header.incl_len

    def close(self):
        """Closes this :class:``PCapStream`` by closing the underlying Python
        stream."""
        if self._stream:
            values = (self._total.nbytes, self._total.npackets, int(math.ceil(self._total.nseconds)), self._filename)
            if self._dryrun:
                msg = 'Would write {} bytes, {} packets, {} seconds to {}.'
            else:
                msg = 'Wrote {} bytes, {} packets, {} seconds to {}.'
                self._stream.close()
            log.info(msg.format(*values))
            self._filename = None
            self._startTime = None
            self._stream = None
            self._total = PCapFileStats(0, 0, 0)