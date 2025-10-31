
from abc import ABC, abstractmethod


class PowerManagementObserver(ABC):
    '''
    Base class for PowerManagement observers.
    Do not make assumptions in what thread or event loop these methods are called.
    '''
    @abstractmethod
    def on_power_sources_change(self, power_management):
        '''
        @param power_management: Instance of PowerManagement posted notification
        '''
        pass

    @abstractmethod
    def on_time_remaining_change(self, power_management):
        '''
        @param power_management: Instance of PowerManagement posted notification
        '''
        pass
