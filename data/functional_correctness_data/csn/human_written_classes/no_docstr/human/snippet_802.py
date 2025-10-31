from stsci.tools import configobj
import functools
import logging

class WithLogging:

    def __init__(self):
        self.depth = 0

    def __call__(self, func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            from .processInput import processFilenames
            errorobj = None
            filename = None
            if self.depth == 0:
                try:
                    configobj = args[0] if args else args
                    if isinstance(configobj, dict) and 'input' in configobj:
                        images = processFilenames(configobj['input'])
                        inputs, output, _, _ = images
                        if output is not None:
                            default = output
                        elif inputs:
                            default = inputs[0]
                        else:
                            default = None
                        filename = configobj.get('runfile', default)
                        if configobj.get('verbose', False):
                            verbose_level = logging.DEBUG
                        else:
                            verbose_level = logging.INFO
                    else:
                        filename = '{}.log'.format(func.__name__)
                        filename = kwargs.get('runfile', filename)
                        debug = kwargs.get('debug', False)
                        verbose = kwargs.get('verbose', False)
                        if debug or verbose:
                            verbose_level = logging.DEBUG
                        else:
                            verbose_level = logging.INFO
                    filename = init_logging(filename, level=verbose_level)
                except (KeyError, IndexError, TypeError):
                    pass
            self.depth += 1
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                errorobj = e
                result = None
                raise
            finally:
                self.depth -= 1
                if self.depth == 0:
                    end_logging(filename)
                    if errorobj:
                        raise errorobj
            return result
        return wrapper