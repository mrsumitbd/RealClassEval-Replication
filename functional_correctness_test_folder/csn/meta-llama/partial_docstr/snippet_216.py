
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

# Example implementation of the abstract class


class ConcretePowerManagementObserver(PowerManagementObserver):
    def on_power_sources_change(self, power_management):
        print("Power sources changed:", power_management)

    def on_time_remaining_change(self, power_management):
        print("Time remaining changed:", power_management)

# Example usage


class PowerManagement:
    def __init__(self):
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_power_sources_change(self):
        for observer in self.observers:
            observer.on_power_sources_change(self)

    def notify_time_remaining_change(self):
        for observer in self.observers:
            observer.on_time_remaining_change(self)


def main():
    power_management = PowerManagement()
    observer = ConcretePowerManagementObserver()
    power_management.register_observer(observer)
    power_management.notify_power_sources_change()
    power_management.notify_time_remaining_change()


if __name__ == "__main__":
    main()
