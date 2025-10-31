import logging
import time

class ProfiledViewMixin:
    """Helper for profiling class-based views

    To use it, make your view inherit from ProfiledViewMixin, then set profiling_mode attribute of your class to desired
    value. The choices are:

    - PROFILING_LOGGING - Simply logs elapsed time with standard logging lib.
    - PROFILING_YAPPI - Uses yappi (https://code.google.com/p/yappi/) to dump detailed profiling data into file. The
      file can be read with KCachegrind. yappi must be installed separately - `pip install yappi`. KCachegrind or
      QCachegrind (on OSX) can be installed via apt or Homebrew.
    """
    PROFILING_OFF = 1
    PROFILING_LOGGING = 2
    PROFILING_YAPPI = 3
    profiling_mode = PROFILING_OFF

    def dispatch(self, request, *args, **kwargs):
        if self.profiling_mode == self.PROFILING_LOGGING:
            return self.dispatch_logging(request, *args, **kwargs)
        if self.profiling_mode == self.PROFILING_YAPPI:
            return self.dispatch_yappi(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def dispatch_logging(self, request, *args, **kwargs):
        logging.info('STARTING %s request', self.__class__.__name__)
        _start = time.time()
        ret = super().dispatch(request, *args, **kwargs)
        _elapsed = time.time() - _start
        logging.info('DONE %s request:  %.1f ms', self.__class__.__name__, _elapsed * 1000)
        return ret

    def dispatch_yappi(self, request, *args, **kwargs):
        with profile_yappi(self.__class__.__name__):
            return super().dispatch(request, *args, **kwargs)