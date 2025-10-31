
from abc import ABC, abstractmethod


class PowerManagementObserver(ABC):
    @abstractmethod
    def on_power_sources_change(self, power_management):
        """Called when the power sources change."""
        pass

    @abstractmethod
    def on_time_remaining_change(self, power_management):
        """Called when the remaining time changes."""
        pass
