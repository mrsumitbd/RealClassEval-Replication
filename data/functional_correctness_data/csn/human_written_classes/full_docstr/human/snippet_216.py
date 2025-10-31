from abc import ABCMeta, abstractmethod

class PowerManagementObserver:
    """
    Base class for PowerManagement observers.
    Do not make assumptions in what thread or event loop these methods are called.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def on_power_sources_change(self, power_management):
        """
        @param power_management: Instance of PowerManagement posted notification
        """
        pass

    @abstractmethod
    def on_time_remaining_change(self, power_management):
        """
        @param power_management: Instance of PowerManagement posted notification
        """
        pass