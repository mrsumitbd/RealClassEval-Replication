
from abc import ABC, abstractmethod


class PowerManagementObserver(ABC):

    @abstractmethod
    def on_power_sources_change(self, power_management):
        pass

    @abstractmethod
    def on_time_remaining_change(self, power_management):
        pass
