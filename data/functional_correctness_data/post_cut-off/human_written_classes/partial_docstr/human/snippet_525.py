from typing import Any, Callable, ClassVar, List, Generic, TypeVar, Dict, Optional, Set, Union
from fletx.utils import get_logger

class Observer:
    """
    Enhanced Observer with Lifecycle Management.
    An advanced observer that allows tracking changes in data 
    while managing the observation lifecycle, including creation, 
    update, and disposal of subscriptions.
    """

    def __init__(self, callback: Callable[[], None], auto_dispose: bool=True):
        self.callback = callback
        self.active = True
        self.auto_dispose = auto_dispose
        self._dependencies = set()
        self._logger = get_logger('FletX.Observer')

    @property
    def logger(self):
        if not self._logger:
            self._logger = get_logger('FletX.Observer')
        return self._logger

    def add_dependency(self, dependency):
        """
        Adds a reactive dependency.
        Registers a new reactive dependency, 
        allowing to track and react to changes in the associated data.
        """
        self._dependencies.add(dependency)

    def notify(self):
        """
        Notifies the observer
        Sends a notification to the observer when the associated data changes, 
        triggering an update or appropriate action.
        """
        if self.active and self.callback:
            try:
                self.callback()
            except Exception as e:
                self.logger.error(f'Observer error: {e}', exc_info=True)

    def dispose(self):
        """
        Cleans up resources
        Releases and cleans up associated resources, 
        such as subscriptions, references, or memory, 
        to prevent memory leaks and optimize performance.
        """
        self.active = False
        self.callback = None
        for dep in self._dependencies:
            dep._remove_observer(self)
        self._dependencies.clear()