from selenium.webdriver.remote.webdriver import WebDriver
import inspect
import typing_extensions as typing
from selene.common.data_structures import persistent
from typing_extensions import Callable, Optional, Any, TypeVar, Dict, Literal, cast, Tuple

class _ManagedDriverDescriptor:

    def __init__(self, *, default: typing.Union[Optional[WebDriver], ...]=...):
        self.default = default
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        config = typing.cast(Config, instance)
        driver_box = typing.cast(persistent.Box[WebDriver], getattr(config, self.name))
        if driver_box.value is None or driver_box.value is ... or (config.rebuild_not_alive_driver and (not callable(driver_box.value)) and (not config._is_driver_alive_strategy(driver_box.value))):
            driver = config.build_driver_strategy(config)
            driver_box.value = driver
            config._schedule_driver_teardown_strategy(config, lambda: driver)
        value = driver_box.value
        if callable(value):
            return value()
        return value

    def __set__(self, instance, value):
        config = typing.cast(Config, instance)
        if not hasattr(instance, self.name):
            if isinstance(value, persistent.Box):
                driver_box = value
            elif inspect.isdatadescriptor(value):
                if type(value) is type(self):
                    driver_box = persistent.Box(self.default)
                else:
                    raise TypeError('Providing custom descriptor objects on init to customize driver management is not supported, because it would be too limited... You would be able to provide it only on init,and use it only via attribute access,without possibility to override value with `persistent.replace` or `config.with_(**options_to_override)`. If you want to use custom descriptor, you have to subclass Config and provide your descriptor objecton class attributes definition level.')
            else:
                driver_box = persistent.Box(value)
                if not callable(value):
                    config._schedule_driver_teardown_strategy(config, lambda: value)
            setattr(instance, self.name, driver_box)
        else:
            driver_box = getattr(instance, self.name)
            driver_box.value = value
            if not callable(value):
                config._schedule_driver_teardown_strategy(config, lambda: value)