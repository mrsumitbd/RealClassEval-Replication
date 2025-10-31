from abc import ABCMeta, abstractmethod

class PersistenceBackend:
    """
    A global abstract class representing an I/O manager for buffer objects containing
    raw measurements.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def load_to_buffer(self):
        """
        Reads meteostation measurement data into a *pyowm.stationsapi30.buffer.Buffer*
        object.

        :returns: a *pyowm.stationsapi30.buffer.Buffer* instance

        """
        pass

    @abstractmethod
    def persist_buffer(self, buffer):
        """
        Saves data contained into a *pyowm.stationsapi30.buffer.Buffer* object
        in a durable form.

        :param buffer: the Buffer object to be persisted
        :type buffer:  *pyowm.stationsapi30.buffer.Buffer* instance

        """
        pass

    def __repr__(self):
        return '<%s.%s>' % (__name__, self.__class__.__name__)