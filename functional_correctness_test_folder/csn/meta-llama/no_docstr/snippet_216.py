
from abc import ABC, abstractmethod


class PowerManagementObserver(ABC):

    @abstractmethod
    def on_power_sources_change(self, power_management):
        pass

    @abstractmethod
    def on_time_remaining_change(self, power_management):
        pass


class ConcretePowerManagementObserver(PowerManagementObserver):
    def __init__(self, name):
        self.name = name

    def on_power_sources_change(self, power_management):
        print(f"{self.name} observed power sources change: {power_management}")

    def on_time_remaining_change(self, power_management):
        print(f"{self.name} observed time remaining change: {power_management}")


class PowerManagement:
    def __init__(self):
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def unregister_observer(self, observer):
        self.observers.remove(observer)

    def notify_power_sources_change(self):
        for observer in self.observers:
            observer.on_power_sources_change(self)

    def notify_time_remaining_change(self):
        for observer in self.observers:
            observer.on_time_remaining_change(self)


def main():
    power_management = PowerManagement()

    observer1 = ConcretePowerManagementObserver("Observer 1")
    observer2 = ConcretePowerManagementObserver("Observer 2")

    power_management.register_observer(observer1)
    power_management.register_observer(observer2)

    power_management.notify_power_sources_change()
    power_management.notify_time_remaining_change()

    power_management.unregister_observer(observer2)

    power_management.notify_power_sources_change()
    power_management.notify_time_remaining_change()


if __name__ == "__main__":
    main()
