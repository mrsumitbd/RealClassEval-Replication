from abc import ABC, abstractmethod
from typing import Any


class PowerManagementObserver(ABC):
    '''
    Base class for PowerManagement observers.
    Do not make assumptions in what thread or event loop these methods are called.
    '''

    @abstractmethod
    def on_power_sources_change(self, power_management: Any) -> None:
        '''
        @param power_management: Instance of PowerManagement posted notification
        '''
        raise NotImplementedError

    @abstractmethod
    def on_time_remaining_change(self, power_management: Any) -> None:
        '''
        @param power_management: Instance of PowerManagement posted notification
        '''
        raise NotImplementedError
